import "../styles/globals.css";
import type { AppProps } from "next/app";
import { CssBaseline, NoSsr, ThemeProvider } from "@mui/material";
import theme from "../styles/theme";
import { CacheProvider } from "@emotion/react";
import createEmotionCache from "../util/clientSideEmotionCache";
import { Provider } from "react-redux";
import { store } from "../models/store";

export default function App({ Component, pageProps }: any) {
  return (
    <NoSsr>
      <ThemeProvider theme={theme}>
        <Provider store={store}>
          <CssBaseline />
          <Component {...pageProps} />
        </Provider>
      </ThemeProvider>
    </NoSsr>
  );
}
