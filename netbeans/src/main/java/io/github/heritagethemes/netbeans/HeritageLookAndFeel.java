package io.github.heritagethemes.netbeans;

import com.formdev.flatlaf.IntelliJTheme;
import java.io.IOException;
import java.io.InputStream;
import java.io.UncheckedIOException;
import javax.swing.UIDefaults;

/**
 * A FlatLaf look and feel over a Heritage theme's IntelliJ UI theme, which names the theme's editor colour profile.
 */
public abstract class HeritageLookAndFeel extends IntelliJTheme.ThemeLaf {

    /** The UI default in which NetBeans looks up the editor colour profile that suits a look and feel. */
    private static final String PREFERRED_PROFILE = "nb.preferred.color.profile";

    private final String name;

    /**
     * @param slug the theme's slug, which names its UI theme resource
     * @param name the theme's name, which is also the display name of its editor colour profile
     */
    protected HeritageLookAndFeel(String slug, String name) {
        super(load(slug));
        this.name = name;
    }

    private static IntelliJTheme load(String slug) {
        String resource = "themes/" + slug + ".theme.json";
        try (InputStream in = HeritageLookAndFeel.class.getResourceAsStream(resource)) {
            if (in == null) {
                throw new IllegalStateException("Missing " + resource);
            }
            return new IntelliJTheme(in);
        } catch (IOException e) {
            throw new UncheckedIOException(e);
        }
    }

    @Override
    public String getName() {
        return name;
    }

    @Override
    public String getDescription() {
        return name;
    }

    @Override
    public UIDefaults getDefaults() {
        UIDefaults defaults = super.getDefaults();
        defaults.put(PREFERRED_PROFILE, name);
        return defaults;
    }
}
