import {
  CustomPaletteOptions,
  PaletteOptions,
  Theme as T,
  ThemeOptions,
  Palette,
  TypeBackground,
} from "@mui/material/styles";

declare module "@mui/material/styles" {
  interface CustomPaletteOptions extends Palette {
    primary: Palette["primary"];
    secondary: Palette["secondary"];
    tertiary: Palette["tertiary"];
    light: Palette["light"];
    dark: Palette["dark"];
    borderColor: Palette["borderColor"];
  }

  interface CustomTheme extends T {
    palette: CustomPaletteOptions;
  }

  // allow configuration using `createTheme`
  interface CustomThemeOptions extends ThemeOptions {
    palette: CustomPaletteOptions;
    background: TypeBackground;
  }
  export function createTheme(options?: CustomThemeOptions): CustomTheme;
}

declare module "@emotion/react/types" {
  interface Theme extends T {
    palette: CustomPaletteOptions;
  }
}
