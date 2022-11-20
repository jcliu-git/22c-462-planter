import {
  AppBar,
  Box,
  CustomTheme,
  IconButton,
  Toolbar,
  Typography,
  useTheme,
} from "@mui/material";

import { Menu } from "@mui/icons-material";
import { useDispatch } from "react-redux";
import { Dispatch } from "../models/store";

export function Masthead() {
  const dispatch = useDispatch<Dispatch>();
  const theme = useTheme<CustomTheme>();
  return (
    <Box sx={{ flexGrow: 1 }}>
      <AppBar position="static" enableColorOnDark={true} color="primary">
        <Toolbar>
          <IconButton
            size="large"
            edge="start"
            color="inherit"
            aria-label="menu"
            sx={{ mr: 2 }}
            onClick={() => dispatch.drawer.open()}
          >
            <Menu />
          </IconButton>
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            Clever Garden
          </Typography>
        </Toolbar>
      </AppBar>
    </Box>
  );
}
