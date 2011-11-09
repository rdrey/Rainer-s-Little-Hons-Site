/* Author: Rainer

*/


jQuery("pre").html(function(index, html) {
    return html.replace(/^(.*)$/mg, "<span class=\"line\">$1</span>")
});












