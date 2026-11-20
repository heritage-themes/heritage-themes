package io.github.heritagethemes.netbeans;

import javax.swing.UIManager;
import org.openide.modules.ModuleInstall;

/** Adds every Heritage look and feel to the ones that NetBeans offers under Tools | Options | Appearance. */
public final class Installer extends ModuleInstall {

    @Override
    public void validate() {
        // NetBeans sets the look and feel before modules are restored, so the look and feels are installed while
        // modules are validated, as NetBeans' own FlatLaf module does.
        for (UIManager.LookAndFeelInfo info : Themes.ALL) {
            UIManager.installLookAndFeel(info);
        }
    }
}
