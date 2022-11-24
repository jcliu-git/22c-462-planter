import {
  AppBar,
  Box,
  Button,
  CustomTheme,
  IconButton,
  Toolbar,
  Typography,
  useTheme,
} from "@mui/material";

import { Menu } from "@mui/icons-material";
import { useDispatch } from "react-redux";
import { Dispatch } from "../models/store";
import { routes } from "../models/routing";
import { useRouter } from "next/router";

export function Masthead() {
  const dispatch = useDispatch<Dispatch>();
  const theme = useTheme<CustomTheme>();
  const router = useRouter();
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
            {Object.keys(routes).map((text) => (
              <Box
                key={text}
                sx={{
                  padding: `0 ${theme.spacing(2)}`,
                  borderBottom:
                    router.route == routes[text] ? "2px solid white" : "",
                }}
              >
                <Button
                  onClick={() => {
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
