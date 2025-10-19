// function ot1(x,y) {
//     console.log(x+y)
//     return x+y
// }
// ot1(8,9)
/*
注释符号

 */

// // 编码伪加密-base64:
// // 加密
// var a = '我是中国人'
// // 先转为二进制，再转为base64的字符串
// // 在js中直接进行转二进制的函数是Buffer.form(字符串)，然后转字符串的函数是toString('编码格式')
// var data_b64 = Buffer.from(a).toString('base64')
// console.log(data_b64)
//
// // 解密：
// // 把base64字符串再转回为二进制数据，然后再进行二进制的解码操作，得出正常的字符
// var data = Buffer.from(data_b64, 'base64').toString('utf-8')
// console.log(data)

// 算法在js中有专门的库可以提供对应的加密算法方法==》 crypto-js
// 需要下载到node.js解释器中，下载命令为==》 npm install 模块名 --registry https://npm.aliyun.com
// npm install crypto-js --registry https://npm.aliyun.com
// const CryptoJs = require('crypto-js')  // 导入算法库对象
// // 可逆加密-对称加密（AES和DES）：
// /*
// * 进行加密算法操作的步骤一般是4步：
// *   1、把要加密的明文数据、密钥转为二进制数据，再传给算法对象；
// *   2、然后设置对应算法的加密模式和填充物的参数，再传给算法对象；
// *   3、然后构建算法对象，并把四个部分传进去执行加密，
// *   4、最后把加密出来的数据再进行转码操作（第三层加密），得出的字符串数据才可以在互联网中进行传输、存储和打印。
//  */
// // 先给要加密的明文和密钥：
// var data = '我是中国人'
// var key = '1234567890asdfgh'  // 密钥必须是16位字节、24位字节或32位字节
// // 再把明文和密钥转为二进制数据，crypto-js算法库中提供的转换方式==》
// var new_data = CryptoJs.enc.Utf8.parse(data)
// var new_key = CryptoJs.enc.Utf8.parse(key)
// // 设置对应算法的加密模式和填充物的参数,可以创建一个对象（字典）来设置：
// var options = {
//     iv: CryptoJs.enc.Utf8.parse('0987654321mnbvc'),     // 当模式是CBC时，需要提供一个初始化向量，必须是16位字节
//     mode: CryptoJs.mode.CBC,   // 设置加密模式为CBC
//     padding: CryptoJs.pad.Pkcs7// 设置填充物为Pkcs7
// }
// // 然后构建算法对象，并把四个部分传进去执行加密，
// // 创建AES或DES算法对象的方法是==》 CryptoJs.AES.encrypt(二进制的明文， 二进制的密钥，模式参数，options对象)
// // var AES_en = CryptoJs.AES.encrypt(new_data, new_key, options)
// var DES_en = CryptoJs.DES.encrypt(new_data, new_key, options)
// // 上面执行算法对象的加密时，会自动进行第三层的转码操作（通常是base64编码）
// // 所以这个加密后的数据如果要打印为正常的字符串就需要使用toString()再转回为普通字符
// // var AES_en_data = AES_en.toString()
// var DES_en_data = DES_en.toString()
// // console.log(AES_en_data)
// console.log(DES_en_data)
// // 解密：AES或DES
// // 创建AES或DES算法对象的方法是==》 CryptoJs.AES.decrypt(密文， 二进制的密钥，模式参数，options对象)
// // var Aes_de = CryptoJs.AES.decrypt(AES_en_data, new_key, options)
// var Des_de = CryptoJs.DES.decrypt(DES_en_data, new_key, options)
// // var AES_de_data = Aes_de.toString(CryptoJs.enc.Utf8)
// var DES_de_data = Des_de.toString(CryptoJs.enc.Utf8)
// // console.log(AES_de_data)
// console.log(DES_de_data)

// 不可逆加密-MD5和SHA1算法（签名算法）：
const CrytoJs = require('crypto-js')  // 导入算法库对象
// 提供明文：
var data = '我是中国人'
// MD5的加密：CryptoJs.MD5(明文数据)
var md5_en = CrytoJs.MD5(data)
// 因为加密后的结果是一个32位的十六进制字符串对象，所以是不能直接看数据和传输的，需要再转为可读的字符串
var md5_en_data = md5_en.toString()
console.log(md5_en_data)

// SHA1的加密：CryptoJs.SHA1(明文数据)
var sha1_en = CrytoJs.SHA1(data)
// 因为加密后的结果是一个32位的十六进制字符串对象，所以是不能直接看数据和传输的，需要再转为可读的字符串
var sha1_en_data = sha1_en.toString()
console.log(sha1_en_data)





