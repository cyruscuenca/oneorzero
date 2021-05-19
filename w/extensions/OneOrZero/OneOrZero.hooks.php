<?php

namespace MediaWiki\Extensions\OneOrZero;

use MediaWiki\MediaWikiServices;
use MediaWiki\Revision\RenderedRevision;
use User;
use CommentStoreComment;
use Status;
use RawMessage;

class Hooks
{
    public static function onBeforePageDisplay(\OutputPage &$outputPage, \Skin &$skin)
    {
        $outputPage->addModuleStyles('zzz.ext.oneorzero.styles');
    }

    public static function onAfterFinalPageOutput(\OutputPage $outputPage)
    {
        // Insert the navigation right after the <body> element
        $out = preg_replace(
            '/(<body[^>]*>)/s',
            '$1' . self::geNavBar(),
            ob_get_clean()
        );

        ob_start();
        echo $out;
        return true;
    }
    
    // Update One or Zero product database when product pages are updated
    public static function onEditFilter($editor, $text, $section, &$error, $summary) { 

        $response = self::httpPost("http://localhost:1738/madeline", ['data' => json_encode(['title' => $editor->getTitle(), 'wikiPage' => $text, 'token' => 'SEhKm2D4k0quCZYs6rsh'])]);
        $response = json_decode($response, true);

        if ($response == '') {

            $error = '<li class="edit-error">' . "ERROR: The edit validation service cannot be reached. Please contact User:Jobgh to get this issue resolved." . "</li>";
            return true;
        }

        if (json_encode($response) != '{"message":"success"}') {

            $error = '<li class="edit-error">' . $response['message'] . "</li>";
        }

        // $response should be true on success, and false on fail
        // false cancels the article save
        return true;
    }

    private static function geNavBar(): string
    {
        $config = MediaWikiServices::getInstance()->getConfigFactory()->makeConfig('oneorzero');
        $NavBar = $config->get("NavBar");
        $OneOrZeroHome = $config->get("OneOrZeroHome");
        $NavBarSelected = $config->get("NavBarSelected");
        $NavBarSelectedDefault = $config->get("NavBarSelectedDefault");

        ob_start();
        // include __DIR__ . '/NavBar2.php';
        return ob_get_clean();
    }

    private static function httpPost($url, $data)
    {
        $curl = curl_init($url);
        curl_setopt($curl, CURLOPT_POST, true);
        curl_setopt($curl, CURLOPT_POSTFIELDS, http_build_query($data));
        curl_setopt($curl, CURLOPT_RETURNTRANSFER, true);
        $response = curl_exec($curl);
        curl_close($curl);
        return $response;
    }    
}
