<?php

namespace MediaWiki\Extensions\OneOrZero;

?>

<style>
#global-nav {
    width: 100%;
    height: auto;
    position: relative;
    top: 0;
    z-index: 99;
}

#page-nav {
    background: #073642;
    width: 100%;
    height: 35px;
}

#nav {
    width: 100%;
    height: 50px;
    display: grid;
    grid-template-rows: 1fr;
    grid-template-columns: 200px calc(600px + 20px) 1fr;
    background: #073642;
    box-sizing: border-box;
}

#nav .horiz-list {
    height: 100%;
    margin: 0;
    text-align: left;
    padding-left: 25px;
}

#nav .horiz-list li {
    height: 100%;
    display: inline-block;
    vertical-align: middle;
    position: relative;
}

#nav .horiz-list li a {
    margin-top: 10px;
    font-size: 12pt;
}

.logo {
    position: relative;
}

.logo img {
    position: relative;
    display: block;
    margin: 10px auto;
    margin-left: 22px;
    height: 30px;
}

.horiz-list li a {
    padding: 6px 12px;
    display: inline-block;
    margin-top: 15px;
    font-weight: 500;
    color: #93a1a1;
}

* {
    font-family: 'Ubuntu';
    font-weight: 400;
    color: #626567;
    list-style-type: none;
    padding: 0;
}

a {
    color: #5dade2;
    text-decoration: none;
}

a:hover {
    text-decoration: none;
}

#constrain {
    position: relative;
    max-width: 1600px;
    margin: 0 auto;
}
</style>

<nav id="global-nav" class="no-select">
    <div id="nav">
        <a class="logo" href='/'>
            <img src="https://wiki.oneorzero.org/view/Special:FilePath/One_or_Zero_Logo.png?height=30">
        </a>
        <div></div>
        <ul class="horiz-list">
            <li>
                <a href="/">
                    Search
                </a>
            </li>
            <li>
                <a href="/wiki" style="color: #f8f9f9;">
                    Wiki
                </a>
            </li>
        </ul>
    </div>
    <div id="page-nav">

    </div>
</nav>

<img id="profile-pic-hack" src="/images/e/e8/Account-inactive.png"/>

<script>
document.getElementById('profile-pic-hack').onclick = function (e) {

    var menu = document.getElementById('p-personal');

    if (getComputedStyle(menu).display == 'none') {

        menu.style.display = 'block';
    } else {

        menu.style.display = 'none';
    }
};
</script>