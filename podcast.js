const got = require('@/utils/got');
const JSONbig = require('json-bigint');
const utils = require('./utils');
const { parseDate } = require('@/utils/parse-date');
const { fallback, queryToBoolean } = require('@/utils/readable-social');
const cache = require('./cache');

/**
    @by CaoMeiYouRen 2020-05-05 添加注释
    注意1：以下均以card为根对象
    注意2：直接动态没有origin，转发动态有origin
    注意3：转发动态格式统一为：
        - user.uname: 用户名
        - item.content: 正文
        - item.tips: 原动态结果(例如：源动态已被作者删除、图文资源已失效)
        - origin: 与原动态一致
    注意4：本总结并不保证完善，而且未来B站可能会修改接口，因此仅供参考

    B站的动态种类繁多，大致可以总结为以下几种：
    - 视频动态
        - aid: av号（以card为根对象没有bv号）
        - owner.name :用户名
        - pic: 封面
        - title: 视频标题
        - desc: 视频简介
    - 音频动态
        - id: auId 音频id
        - upper: 上传的用户名称
        - title: 音频标题
        - author: 音频作者
        - cover: 音频封面
*/

module.exports = async (ctx) => {
    const {uid, useAvid = true} = ctx.params;

    const response = await got({
        method: 'get',
        url: `https://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/space_history?host_uid=${uid}`,
        headers: {
            Referer: `https://space.bilibili.com/${uid}/`,
        },
        transformResponse: [(data) => data],
    });
    const cards = JSONbig.parse(response.body).data.cards;
    const usernameAndFace = await cache.getUsernameAndFaceFromUID(ctx, uid);
    const author = usernameAndFace[0] ?? cards[0]?.desc?.user_profile?.info.uname;
    const face = usernameAndFace[1] ?? cards[0]?.desc?.user_profile?.info?.face;

    ctx.cache.set(`bili-username-from-uid-${uid}`, author);
    ctx.cache.set(`bili-userface-from-uid-${uid}`, face);

    const items = await Promise.all(
        cards.map(async (item) => {
            const data = JSONbig.parse(item.card);
            if (!data) {
                return null;
            }
            
            const desc = data.desc;
            const aid = data.aid;
            const bvid = item?.desc?.bvid || item?.desc?.origin?.bvid;
            const cid = data.cid;
            const pic = data.pic;
            const ctime = data.ctime;

            const video_response = await got({
                method: 'get',
                url: `https://api.bilibili.com/x/player/playurl?avid=${aid}&cid=${cid}&qn=16&otype=json&fourk=1&fnver=0&fnval=4048`,
                headers: {
                    Referer: `https://space.bilibili.com/${uid}/`,
                    Host: 'api.bilibili.com',
                    Origin: 'https://www.bilibili.com',
                    Connection: 'keep-alive'
                },
                transformResponse: [(data) => data],
            });
            let video_response_json = JSONbig.parse(JSONbig.stringify(video_response.body));
            console.log(video_response_json.data);
            let audio_url = video_response_json.data.dash.audio[0].base_url;
            return {
                title: desc,
                pubDate: parseDate(ctime, 'X'),
                itunes_item_image: pic, // 条目的封面图像
                itunes_duration: '', // 可选，音频的长度，以秒为单位 或 H:mm:ss 格式
                enclosure_url: audio_url, // 音频直链
                enclosure_length: '', // 可选，文件大小，以 Byte 为单位
                enclosure_type: 'audio/x-m4a', // 音频文件 MIME 类型（常见类型 .mp3 是 'audio/mpeg'，.m4a 是 'audio/x-m4a'，.mp4 是 'video/mp4'）
            };
        })
    );

    ctx.state.data = {
        itunes_author: `${author}`,
        itunes_category: `bilibili`,
        title: `${author} 的 bilibili podcast`,
        link: `https://space.bilibili.com/${uid}/video`,
        description: `由 ${author} 的 bilibili 投稿视频转换而来的播客`,
        image: face,
        item: items,
    };
};
