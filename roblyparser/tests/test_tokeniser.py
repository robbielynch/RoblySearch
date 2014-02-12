from unittest import TestCase
from roblyparser.tokeniser import Tokens
__author__ = 'robbie'


class TestTokeniser(TestCase):

    html = """
    <html>
    <head>
        <title>My HTML Page</title>
    </head>
    <body>
        <p style="special">
            This paragraph has special style
        </p>
        <p>
            This paragraph is not special
        </p>
    </body>
    </html>
    """

    def setUp(self):
        pass

    def test_tokenise(self):
        t = Tokens()
        tokens = t.tokenise(hhh)
        #tokens = t.tokenise(self.html)
        print("done")

    def test_get_tag(self):
        t = Tokens()
        h = "hello<head>stuff</head>"
        tag = t.get_tag(h, 5)
        print("")

    def test_get_string_content(self):
        t = Tokens()
        h = "<head>stuff</head>"
        tag = t.get_string_content(h, 5)
        print("")
        self.assertEqual(("stuff", 6,), tag)


    def tearDown(self):
        pass


hhh = """

<!DOCTYPE html>
<html class="no-js" lang="en">
  <head>
    <meta charset="utf-8">
    <meta content=
    "width=device-width,initial-scale=1.0,minimum-scale=1.0,maximum-scale=1.0,user-scalable=no,target-densitydpi=160"
    name="viewport">
    <meta content="IE=edge" http-equiv="X-UA-Compatible">
    <meta content="Android" name="title">
    <meta content="Android - Homepage" name="description">
    <title>
      Android
    </title>
    <link href="//fonts.googleapis.com/css?family=Roboto:400,300,100" rel="stylesheet">
    <link href="./new/images/favicon.ico" rel="shortcut icon">
    <link href="./new/images/touch-icon-iphone.png" rel="apple-touch-icon">
    <link href="./new/images/touch-icon-ipad.png" rel="apple-touch-icon" sizes="76x76">
    <link href="./new/images/touch-icon-iphone-retina.png" rel="apple-touch-icon" sizes="120x120">
    <link href="./new/images/touch-icon-ipad-retina.png" rel="apple-touch-icon" sizes="152x152">
    <link href="./new/stylesheets/site.min.css" rel="stylesheet">
    <script src="//www.gstatic.com/external_hosted/modernizr/modernizr.js">
</script>
    <script src="//www.google.com/js/gweb/analytics/autotrack.js">
</script>
    <script>
new gweb.analytics.AutoTrack({
        profile: 'UA-5686560-1'
      });
    </script>
  </head>
  <body class="index">
    <div class="header js-search-close">
      <div class="header__item with-site-logo js-search-close">
        <div class="site-logo site-logo--in-header three-twelfths mobile-five-sixths">
          <a class="site-logo__link site-logo__link--in-header" href="/">
          <div class="site-logo__image icon icon--logo">
            Android
          </div></a>
        </div>
      </div>
      <div class="basement__toggle header__item mobile-one-sixth with-icon js-basement-toggle"
      data-target-basement="mobile">
        <div class="icon icon--mobile"></div>
      </div>
      <div class="header__item with-nav with-search js-search-container">
        <div class="nav nav--horizontal nav--active-page-labels nine-twelfths js-search--fadable"
        role="navigation">
          <a class="nav__item nav__item--first nav__item--android" href="/meet-android/">
          <div class="nav__label">
            Meet Android
          </div></a> <a class="nav__item nav__item--apps" href="/apps-and-entertainment/">
          <div class="nav__label">
            Apps &amp; Entertainment
          </div></a> <a class="nav__item nav__item--devices" href="/phones-and-tablets/">
          <div class="nav__label">
            Phones &amp; Tablets
          </div></a>
          <div class="nav__item nav__item--search with-search">
            <div class="nav__label">
              <div class="icon-wrapper--search js-search-open">
                <div class="icon icon--search"></div>
              </div>
            </div>
          </div>
        </div>
        <form action="./results" class="search search--within-header with-icon js-search-form" id=
        "search" method="get" name="search">
          <div class="search__submit-wrapper js-search-submit">
            <div class="search__submit icon icon--search"></div>
          </div><label for="q">Search</label> <input class="search__input js-search-input" id="q"
          name="q" value="">
        </form>
      </div>
    </div>
    <div class="page page--wrapper js-basement-wrapper">
      <div class="page-content js-basement-under">
        <div class="js-search-close">
          <div class=
          "photo-statement photo-statement--3x2 photo-statement--first js-animate-on-load">
            <div class="photo-statement__photo-wrapper">
              <div class=
              "photo-statement__photo photo-focus--top-right js-responsive-image js-parallax-image"
              data-breakpoints="320,768,1024,1200,1600" data-known-dimensions="false"
              data-preserve-aspect-ratio="false" data-src="/new/images/banners/home1.jpg"></div>
            </div>
            <div class="photo-statement__text-wrapper">
              <a class=
              "photo-statement__text photo-statement__text--bottom-right js-repaint js-photo-statement-text"
              href="/versions/kit-kat-4-4/">
              <h2 class="photo-statement__text-headline">
                Introducing Android 4.4, KitKat
              </h2>
              <p class="photo-statement__text-subhead with-entity">
                Learn about our latest treat
              </p></a>
            </div>
          </div>
          <div class="section section--home section--centered section--top-buffer">
            <h1 class="section__headline text--center">
              Android Updates
            </h1>
            <p class="section__body text--center two-thirds mobile-one-whole">
              The latest news and product updates from our <a class="with-entity" href=
              "https://plus.google.com/+android/">Google+ page</a>
            </p>
          </div>
          <div class="section section--updates section--centered section--mobile-gutterless">
            <div class="updates js-news-content"></div>
            <div class="updates__animation"></div>
          </div>
        </div>
        <div class="footer">
          <div class="footer__content">
            <div class="footer__item one-quarter mobile-one-whole mobile-is-hidden">
              <a class="footer__link" href="/">Home</a> <a class="footer__link" href=
              "/meet-android">Meet Android</a> <a class="footer__link" href=
              "/apps-and-entertainment">Apps &amp; Entertainment</a> <a class="footer__link" href=
              "/phones-and-tablets">Phones &amp; Tablets</a> <a class="footer__link" href=
              "//www.google.com/intl/en/policies/" target="_blank">Privacy &amp; Terms</a>
            </div>
            <div class="footer__item one-quarter mobile-one-whole">
              <a class="footer__link" href="//officialandroid.blogspot.com" target=
              "_blank">Official Blog</a> <a class="footer__link" href="//www.google.com/+android"
              target="_blank">Android on Google+</a> <a class="footer__link" href=
              "//twitter.com/android" target="_blank">Android on Twitter</a>
            </div>
            <div class="footer__item one-quarter mobile-one-whole mobile-is-hidden">
              <div class="footer__label">
                Versions
              </div><a class="footer__link" href="/versions/kit-kat-4-4/">4.4 KitKat</a> <a class=
              "footer__link" href="/versions/jelly-bean-4-3/">4.3 Jelly Bean</a> <a class=
              "footer__link" href="/versions/jelly-bean-4-2/">4.2 Jelly Bean</a>
            </div>
            <div class="footer__item one-quarter mobile-one-whole">
              <div class="footer__label">
                For Developers
              </div><a class="footer__link" href="//developer.android.com/" target=
              "_blank">Developer Resources</a> <a class="footer__link" href=
              "//developer.android.com/sdk" target="_blank">Android SDK</a>
            </div>
            <div class="footer__item footer__item--extra one-quarter mobile-one-half">
              <div class="footer__sharing">
                <div class="g-plusone" data-annotation="none" data-width="300"></div>
              </div>
            </div>
            <div class=
            "footer__item footer__item--extra footer__item--logo three-quarters mobile-one-half text--right">
            <a class="footer__google-logo" href="//google.com" target="_blank">
              <div class="icon icon--google"></div></a>
            </div>
          </div>
        </div>
      </div>
      <div class=
      "basement nav--active-page-labels js-basement js-basement-close js-basement--mobile js-basement-over--mobile"
      data-basement-name="mobile" data-push-content="false" data-slide-direction="right">
        <div class="nav nav--overflow nav--vertical js-search-close js-nav-width">
          <div class="nav__vertical-search js-search-container">
            <div class="nav__item nav__item--site-logo js-search--fadable">
              <div class="nav__label site-logo">
                <a class="site-logo__link" href="/">
                <div class="site-logo__image icon icon--logo"></div></a>
              </div>
            </div>
            <div class="nav__item nav__item--search with-search">
              <div class="nav__label nav__label--vertical-search">
                <div class="icon-wrapper--search js-search-open">
                  <div class="icon icon--search"></div>
                </div>
              </div>
            </div>
            <form action="./results" class=
            "search search--within-basement with-icon js-search-form" method="get">
              <div class=
              "search__submit-wrapper search__submit-wrapper--in-basement js-search-submit">
                <div class="search__submit icon icon--search"></div>
              </div><input class="search__input search__input--in-basement js-search-input" name=
              "q" placeholder="Search">
            </form>
          </div><a class="nav__item nav__item--android" href="/meet-android/">
          <div class="nav__label">
            Meet Android
          </div></a> <a class="nav__item nav__item--apps" href="/apps-and-entertainment/">
          <div class="nav__label">
            Apps &amp; Entertainment
          </div></a> <a class="nav__item nav__item--devices" href="/phones-and-tablets/">
          <div class="nav__label">
            Phones &amp; Tablets
          </div></a>
          <div class="js-nav-expand">
            <div class="nav__item nav__item--last js-nav-expand-toggle">
              <div class="nav__label">
                Versions <span class="icon icon--nav-accordion">&nbsp;</span>
              </div>
            </div>
            <div class="nav__item--submenu js-nav-expanded">
              <a class="nav__item nav__item--first nav__item--kit-kat-4-4" href=
              "/versions/kit-kat-4-4/">
              <div class="nav__label">
                4.4 KitKat
              </div></a> <a class="nav__item nav__item--jelly-bean-4-3" href=
              "/versions/jelly-bean-4-3/">
              <div class="nav__label">
                4.3 Jelly Bean
              </div></a> <a class="nav__item nav__item--jelly-bean-4-2" href=
              "/versions/jelly-bean-4-2/">
              <div class="nav__label">
                4.2 Jelly Bean
              </div></a>
            </div>
          </div>
        </div>
      </div>
    </div><script src="//www.gstatic.com/external_hosted/gsap/TweenMax.min.js">
</script> <script src="//www.gstatic.com/external_hosted/hammerjs/hammer.min.js">
</script> <script src="./new/javascripts/site.min.js">
</script> <script async="" src="//apis.google.com/js/plusone.js">
{"parsetags": "explicit"}
    </script> <script>
android.init('home');
    </script>
  </body>
</html>
"""