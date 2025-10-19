
 function asrsea(id) {
     var id_dict = `{\"ids\":\"[${id}]\",\"level\":\"exhigh\",\"encodeType\":\"aac\",\"csrf_token\":\"5eea58d68166c0ff44bcc67bd99780d5\"}`
     var e = "010001"
     var f = "00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7"
     var g = "0CoJUm6Qyw8W8jud"
     const CryptoJS = require('crypto-js')
     function b(a, b) {
        var c = CryptoJS.enc.Utf8.parse(b)
          , d = CryptoJS.enc.Utf8.parse("0102030405060708")
          , e = CryptoJS.enc.Utf8.parse(a)
          , f = CryptoJS.AES.encrypt(e, c, {
            iv: d,
            mode: CryptoJS.mode.CBC
        });
        return f.toString()
    }
    function d(id_dict, e, f, g) {
        var h = {}
          , i = "4Tkv8GwUXc7LBAC9";
        return h.encText = b(id_dict, g),
        h.encText = encodeURIComponent(b(h.encText, i)),  // 这个字符串中的特殊字符（+、/、=符号）需要被转义为url格式的十六进制才能进行传输
        h.encSecKey = "cbf9ca65faa714173aed79ac4507a2397f58c823af5eee415d4c66e98e96154aae9ebb4734682732c0d431e4bdd73a29df16eadd17f53a1e83afe25f8d2fa3519d04906b979e272fbb9d363ed5a1bd39a45027f87d55e626e2587ca7aa181208d787494fc5af9a3164e3a5218a1715d7b794e5f6c98124d656c8072f1c8cc06e",
            // 这个encSecKey的c函数返回值是去复制跟上面的i值对应生成的字符串
        h
    }
    return d(id_dict, e, f, g)  // 返回值
}