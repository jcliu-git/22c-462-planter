import "../styles/globals.css";
import { CssBaseline, NoSsr, ThemeProvider } from "@mui/material";
import theme from "../styles/theme";
import { Provider, useDispatch } from "react-redux";
import { Dispatch, store } from "../models/store";
import { Navigation } from "../components/navigation";
import { Masthead } from "../components/masthead";
import { useRouter } from "next/router";
import { Socket } from "../models/socket";
import { CleverGardenContext } from "../models/context";

export default function App({ Component, pageProps }: any) {
  const router = useRouter();

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
