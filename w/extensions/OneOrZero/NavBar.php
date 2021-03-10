<?php

namespace MediaWiki\Extensions\OneOrZero;

/**
 * @var \SkinTemplate $skinTemplate
 * @var array $NavBar
 * @var string $Home
 * @var array $NavBarSelected
 * @var string $NavBarSelectedDefault
 */
?>
<div id="archnavbar" class="noprint">
    <div id="archnavbarlogo">
        <p><a id="logo" href="<?= $OneOrZeroHome ?>"></a></p>
    </div>
    <div id="archnavbarmenu">
        <ul id="archnavbarlist">
            <?php
            foreach ($NavBar as $name => $url) {
                if (($skinTemplate->getTitle() == $name && in_array($name, $NavBarSelected))
                    || (!(in_array($skinTemplate->getTitle(), $NavBarSelected)) && $name == $NavBarSelectedDefault)) {
                    $anbClass = ' class="anb-selected"';
                } else {
                    $anbClass = '';
                }
                ?>
            <li id="anb-<?= strtolower($name) ?>"<?= $anbClass ?>><a href="<?= $url ?>"><?= $name ?></a></li><?php
            }
            ?>
        </ul>
    </div>
</div>
