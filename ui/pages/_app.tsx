import "../styles/globals.css";
import type { AppProps } from "next/app";
import { CssBaseline, NoSsr, ThemeProvider } from "@mui/material";
import theme from "../styles/theme";
import { CacheProvider } from "@emotion/react";
import createEmotionCache from "../util/clientSideEmotionCache";
import { Provider } from "react-redux";
import { store } from "../models/store";

const clientSideEmotionCache = createEmotionCache();

export default function App({
  Component,
  pageProps,
  emotionCache = clientSideEmotionCache,
}: any) {
  return (
    <NoSsr>
      <CacheProvider value={emotionCache}>
        <ThemeProvider theme={theme}>
          <Provider store={store}>
            <CssBaseline />
            <Component {...pageProps} />
          </Provider>
        </ThemeProvider>
      </CacheProvider>
    </NoSsr>
  );
}
