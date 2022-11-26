import "../styles/globals.css";
import { CssBaseline, NoSsr, ThemeProvider } from "@mui/material";
import theme from "../styles/theme";
import { Provider, useDispatch } from "react-redux";
import { Dispatch, initStore, store } from "../models/store";
import { Navigation } from "../components/navigation";
import { Masthead } from "../components/masthead";
import { useRouter } from "next/router";
import { Socket } from "../models/socket";
import { CleverGardenContext } from "../models/context";
import Head from "next/head";

export default function App({ Component, pageProps }: any) {
  const router = useRouter();
  initStore();
  return (
    <NoSsr>
      <ThemeProvider theme={theme}>
        <Provider store={store}>
          <Head>
            <meta charSet="utf-8" />
            <meta httpEquiv="X-UA-Compatible" content="IE=edge" />
            <meta
              name="viewport"
              content="width=device-width,initial-scale=1,minimum-scale=1,maximum-scale=1,user-scalable=no"
            />
            <meta name="description" content="Description" />
            <meta name="keywords" content="Keywords" />
            <title>Clever Garden</title>

            <link rel="manifest" href="/manifest.json" />
            {/* <link
              href="/icons/favicon-16x16.png"
              rel="icon"
              type="image/png"
              sizes="16x16"
            />
            <link
              href="/icons/favicon-32x32.png"
              rel="icon"
              type="image/png"
              sizes="32x32"
            /> */}
            {/* <link rel="apple-touch-icon" href="/apple-icon.png"></link> */}
            <meta name="theme-color" content={theme.palette.primary.main} />
          </Head>
          <CssBaseline />
          <Navigation />
          <Masthead />
          <Component {...pageProps} />
        </Provider>
      </ThemeProvider>
    </NoSsr>
  );
}
