import { AppBar, Box, IconButton, Toolbar, Typography } from "@mui/material";

import { Menu } from "@mui/icons-material";
import { useDispatch } from "react-redux";
import { Dispatch } from "../models/store";

export function Masthead() {
  const dispatch = useDispatch<Dispatch>();
  return (
    <Box sx={{ flexGrow: 1 }}>
      <AppBar position="static">
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
