function reply_click(clicked_id)
{
    var x = document.getElementById(clicked_id);

    if (x.className.indexOf("hiddenText") == -1) {
        console.log("if");
        x.className = "hiddenText";
    } else {
        console.log("else");
        x.className = "notHiddenText";
    }
    console.log(x);
}
