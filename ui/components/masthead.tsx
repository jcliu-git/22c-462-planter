import {
  AppBar,
  Box,
  Button,
  CustomTheme,
  IconButton,
  Toolbar,
  useTheme,
} from "@mui/material";

import { Menu } from "@mui/icons-material";
import { useDispatch, useSelector } from "react-redux";
import { Dispatch, RootState } from "../models/store";
import { routes } from "../models/routing";
import { useRouter } from "next/router";

export function Masthead() {
  const dispatch = useDispatch<Dispatch>();
  const theme = useTheme<CustomTheme>();
  const router = useRouter();
  const websocketConnected = useSelector(
    (state: RootState) => state.hub.websocketConnected
  );
  return (
    <Box sx={{ flexGrow: 1 }}>
      <AppBar position="static" enableColorOnDark={true} color="primary">
        <Toolbar>
          <IconButton
            size="large"
            edge="start"
            color="inherit"
            aria-label="menu"
            sx={{ mr: 2, display: { xs: "block", sm: "none" } }}
            onClick={() => dispatch.drawer.open()}
          >
            <Menu />
          </IconButton>
          {/* <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            Clever Garden
          </Typography> */}
          <Box
            sx={{
              flexGrow: 1,
              display: { xs: "none", sm: "flex" },
              justifyContent: "start",
            }}
          >
            {Object.keys(routes)
              .filter((route) => route != "Control Panel" || websocketConnected)
              .map((text) => (
                <Box
                  key={text}
                  sx={{
                    padding: `0 ${theme.spacing(2)}`,
                    borderBottom:
                      router.route == routes[text] ? "2px solid white" : "",
                  }}
                >
                  <Button
                    onClick={async () => {
                      dispatch.drawer.close();
                      router.push(routes[text]);
                    }}
                    sx={{ my: 2, color: "white", display: "block" }}
                  >
                    {text}
                  </Button>
                </Box>
              ))}
          </Box>
        </Toolbar>
      </AppBar>
    </Box>
  );
}
