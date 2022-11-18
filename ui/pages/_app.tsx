import "../styles/globals.css";
import { CssBaseline, NoSsr, ThemeProvider } from "@mui/material";
import theme from "../styles/theme";
import { Provider } from "react-redux";
import { store } from "../models/store";
import { Navigation } from "../components/navigation";
import { Masthead } from "../components/masthead";

export default function App({ Component, pageProps }: any) {
  return (
    <NoSsr>
      <ThemeProvider theme={theme}>
        <Provider store={store}>
          <CssBaseline />
          <Navigation />
          <Masthead />
          <Component {...pageProps} />
        </Provider>
      </ThemeProvider>
    </NoSsr>
  );
}
