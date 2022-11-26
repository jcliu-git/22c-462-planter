import { Box, Drawer, List, ListItem, ListItemText } from "@mui/material";
import { useRouter } from "next/router";
import { useDispatch, useSelector } from "react-redux";
import { routes } from "../models/routing";
import { Dispatch, RootState } from "../models/store";

export function Navigation() {
  const drawerState = useSelector((state: RootState) => state.drawer);
  const websocketConnected = useSelector(
    (state: RootState) => state.hub.websocketConnected
  );
  const dispatch = useDispatch<Dispatch>();
  const router = useRouter();

  return (
    <Drawer
      anchor="left"
      open={drawerState.open}
      onClose={() => dispatch.drawer.close()}
    >
      <Box
        sx={{
          width: 320,
        }}
        role="presentation"
      >
        <List>
          {Object.keys(routes)
            .filter((route) => route != "Control Panel" || websocketConnected)
            .map((text) => (
              <ListItem
                button
                key={text}
                onClick={() => {
                  dispatch.drawer.close();
                  router.push(routes[text]);
                }}
              >
                <ListItemText primary={text} />
              </ListItem>
            ))}
        </List>
      </Box>
    </Drawer>
  );
}
