import { createTheme, CustomThemeOptions } from "@mui/material/styles";
import { red } from "@mui/material/colors";

// Create a theme instance.
const theme = createTheme({
  palette: {
    primary: {
      main: "#357960",
    },
    secondary: {
      main: "#664C43",
    },
    tertiary: {
      main: "#D88C9A",
    },
    light: {
      main: "#F4F3EE",
    },
    dark: {
      main: "#051923",
    },
    error: {
      main: red.A400,
    },

    mode: "dark",
    borderColor: "#131313",
  },
  background: {
    default: "#020202",
    paper: "#24292F",
  },
} as CustomThemeOptions);

export default theme;
