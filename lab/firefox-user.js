// Lab Firefox profile (not filmed as a step): skip the first-run tabs and the default-browser question, draw the UI
// at 2x so text reads on a phone after the zoom, save downloads to ~/Downloads without asking, no telemetry.
user_pref("layout.css.devPixelsPerPx", "2.0");
user_pref("browser.aboutwelcome.enabled", false);
user_pref("trailhead.firstrun.didSeeAboutWelcome", true);
user_pref("browser.startup.homepage_override.mstone", "ignore");
user_pref("startup.homepage_welcome_url", "");
user_pref("startup.homepage_welcome_url.additional", "");
user_pref("browser.shell.checkDefaultBrowser", false);
user_pref("datareporting.policy.dataSubmissionPolicyBypassNotification", true);
user_pref("datareporting.healthreport.uploadEnabled", false);
user_pref("toolkit.telemetry.reportingpolicy.firstRun", false);
user_pref("browser.download.useDownloadDir", true);
user_pref("browser.download.always_ask_before_handling_new_types", false);
user_pref("browser.download.alwaysOpenPanel", true);
user_pref("browser.tabs.firefox-view", false);
user_pref("browser.newtabpage.enabled", false);
user_pref("extensions.pocket.enabled", false);
user_pref("browser.translations.automaticallyPopup", false);
user_pref("sidebar.revamp", false);
user_pref("browser.ml.chat.enabled", false);
user_pref("browser.urlbar.suggest.trending", false);
