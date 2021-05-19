#!/usr/bin/python
"""
This bot goes over multiple pages of a wiki, and edits them without changes.

This is for example used to get category links in templates working.

Command-line arguments:

-purge                    Purge the page instead of touching it

Touch mode (default):

-botflag                  Force botflag in case of edits with changes.

Purge mode:

-converttitles            Convert titles to other variants if necessary
-forcelinkupdate          Update the links tables
-forcerecursivelinkupdate Update the links table, and update the links tables
                          for any page that uses this page as a template
-redirects                Automatically resolve redirects

&params;
"""
#
# (C) Pywikibot team, 2009-2020
#
# Distributed under the terms of the MIT license.
#
import pywikibot

from pywikibot import pagegenerators

from pywikibot.bot import MultipleSitesBot

docuReplacements = {'&params;': pagegenerators.parameterHelp}  # noqa: N816


class TouchBot(MultipleSitesBot):

    """Page touch bot."""

    def __init__(self, generator, **kwargs) -> None:
        """Initialize a TouchBot instance with the options and generator."""
        self.available_options.update({
            'botflag': False,
        })
        super().__init__(generator=generator, **kwargs)

    def treat(self, page) -> None:
        """Touch the given page."""
        try:
            page.touch(botflag=self.opt.botflag)
        except (pywikibot.NoCreateError, pywikibot.NoPage):
            pywikibot.error('Page {0} does not exist.'
                            .format(page.title(as_link=True)))
        except pywikibot.LockedPage:
            pywikibot.error('Page {0} is locked.'
                            .format(page.title(as_link=True)))
        except pywikibot.PageSaveRelatedError:
            pywikibot.error('Page {0} not saved.'
                            .format(page.title(as_link=True)))


class PurgeBot(MultipleSitesBot):

    """Purge each page on the generator."""

    available_options = {
        'converttitles': None,
        'forcelinkupdate': None,
        'forcerecursivelinkupdate': None,
        'redirects': None
    }

    def treat(self, page) -> None:
        """Purge the given page."""
        pywikibot.output('Page {}{} purged'
                         .format(page,
                                 '' if page.purge(**self.opt) else ' not'))


def main(*args) -> None:
    """
    Process command line arguments and invoke bot.

    If args is an empty list, sys.argv is used.

    @param args: command line arguments
    @type args: str
    """
    options = {}

    # Process global args and prepare generator args parser
    local_args = pywikibot.handle_args(args)
    gen_factory = pagegenerators.GeneratorFactory()

    bot_class = TouchBot
    for arg in local_args:
        if gen_factory.handle_arg(arg):
            continue
        if arg == '-purge':
            bot_class = PurgeBot
        elif arg.startswith('-'):
            options[arg[1:].lower()] = True

    if gen_factory.gens:
        gen = gen_factory.getCombinedGenerator(preload=True)
        pywikibot.Site().login()
        bot_class(generator=gen, **options).run()
    else:
        pywikibot.bot.suggest_help(missing_generator=True)


if __name__ == '__main__':
    main()
