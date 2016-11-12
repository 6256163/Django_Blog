/**
 * Created by Administrator on 2016/11/8/008.
 */
String.prototype.replaceAll = function(s1,s2){
return this.replace(new RegExp(s1,"gm"),s2);
}