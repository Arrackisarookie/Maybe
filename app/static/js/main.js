(function() {
    // åŽ»æŽ‰é‡å¤å‡½æ•°ï¼Œåˆ†è£…é¼ æ ‡ç‚¹å‡»æ—¶é—´
    var clickEvent = function(el1, el2) {
        el1.onclick = function() {
            if (el2.style.display === 'none') {
                el2.style.display = 'block';
            } else {
                el2.style.display = 'none';
            }
        }
    };

    // ä¸‹æ‹‰èœå•äº‹ä»¶
    var dropNav = document.getElementById('drop');
    var navCate = document.getElementsByClassName('category-nav')[0];

    // é¼ æ ‡è¿›å…¥
    navCate.onmouseenter = function() {
        dropNav.style.display = 'block';
    };

    // é¼ æ ‡ç¦»å¼€
    navCate.onmouseleave = function() {
        dropNav.style.display = 'none';
    };

    // æœç´¢æ¡†äº‹ä»¶
    var searchNav = document.getElementsByClassName('search-btn')[0];
    var searchDiv = document.getElementsByClassName('search')[0];
    var searchIpt = document.getElementsByClassName('search-ipt')[0];

    // é¼ æ ‡ç‚¹å‡»
    searchNav.onclick = function() {
        if (searchDiv.style.display === 'none') {
            searchDiv.style.display = 'block';
            searchIpt.focus();
        } else {
            searchDiv.style.display = 'none';
        }
    };

    // å›žåˆ°é¡¶éƒ¨
    window.onscroll = function() {
        var toTop = document.getElementById('go-to-top');
        var oldTop = document.documentElement.scrollTop || document.body.scrollTop;
        var timer;
        toTop.onclick = function() {
            var speed = 5;
            timer = setInterval(function() {
                var top = document.documentElement.scrollTop || document.body.scrollTop;
                var goSpeed = top/100;
                if (goSpeed > speed) {
                    goSpeed = speed;
                } else if (goSpeed < 3) {
                    goSpeed = 3;
                }

                if (top > speed) {
                    if(document.documentElement.scrollTop){
                        top = document.documentElement.scrollTop-=speed;
                    }else{
                        top = document.body.scrollTop-=speed;
                    }
                } else {
                    clearInterval(timer);
                }
            }, 0);
        };

        var newTop = document.documentElement.scrollTop || document.body.scrollTop;
        if (newTop > 100) {
            toTop.style.display = 'block';
        } else {
            toTop.style.display = 'none';
        }
        if (newTop > oldTop) {
            clearInterval(timer);
        }
        oldTop = newTop;
    };

    // width < 960px
    // å¯¼èˆªäº‹ä»¶
    var mobileNav = document.getElementsByClassName('mobile-site-nav')[0];
    var mobileBtnDiv = document.getElementsByClassName('mobile-menu-btn')[0];
    var mobileNavBtn = mobileBtnDiv.getElementsByTagName('button')[0];

    clickEvent(mobileNavBtn, mobileNav);

    // åˆ†ç±»æ˜¾ç¤ºä¸‹æ‹‰
    var mobileCate = document.getElementsByClassName('mobile-category')[0];
    var mobileDrop = document.getElementsByClassName('mobile-drop-category')[0];

    clickEvent(mobileCate, mobileDrop);

    // width < 960px user button
    var mobileUserBtn = mobileBtnDiv.getElementsByTagName('button')[1];
    var mobileUser = document.getElementsByClassName('sidebar')[0];

    mobileUserBtn.onclick = function() {
        if (mobileUser.style.display === "none") {
            mobileUser.style.display = "block";
        } else if (mobileUser.style.display === "") {
            mobileUser.style.display = "block";
        } else {
            mobileUser.style.display = "none";
        }
    };

    // love me sidebar
    var loveMeTitle = document.getElementsByClassName('love-title')[0];
    var loveMe = document.getElementsByClassName('love-me-icon')[0];
    var loveMeCount = document.getElementsByClassName('love-me-count')[0];
    var counts = parseInt(loveMeCount.innerText);

    var request;
    if (window.XMLHttpRequest) {
        request = new XMLHttpRequest();
    } else {
        request = new ActiveXObject('Microsoft.XMLHTTP');
    }

    loveMe.onclick = function() {
        // åˆ¤æ–­æœ¬åœ°æ˜¯å¦æœ‰ç™»å½•è®°å½•
        var love = ms.get('love');
        if (love) {
            loveMeTitle.innerHTML = 'æˆ‘çŸ¥é“ä½ å–œæ¬¢æˆ‘';
        } else {
            ms.set('love', 'loved');
            counts += 1;
            loveMeTitle.innerHTML = 'æˆ‘ä¹Ÿå–œæ¬¢ä½ ';
            loveMeCount.innerText = counts.toString();

            // å‘é€è¯·æ±‚:
            FormData = JSON.stringify({i_am_handsome: 'yes'});
            request.open('POST', '/loveme');
            request.setRequestHeader('Content-Type', 'application/json');
            request.send(FormData);
        }
    };

    // ä¾§æ æ¦‚è§ˆå’Œæ–‡ç« ç›®å½•çš„æ˜¾ç¤º
    var sideNav = document.getElementsByClassName('side-nav')[0];
    var tocBtn = sideNav.getElementsByTagName('span')[0];
    var viewBtn = sideNav.getElementsByTagName('span')[1];
    var tocBox = document.getElementsByClassName('post-toc')[0];
    var viewBox = document.getElementsByClassName('profile')[0];

    tocBtn.onclick = function() {
        viewBtn.className = "";
        this.className = "current";
        viewBox.style.display = "none";
        tocBox.style.display = "block";
    };
    viewBtn.onclick = function() {
        tocBtn.className = "";
        this.className = "current";
        tocBox.style.display = "none";
        viewBox.style.display = "block";
    };

})();
