import {
  Card,
  CustomTheme,
  Grid,
  List,
  ListItem,
  ListItemText,
  Slider,
  Stack,
  Typography,
  useTheme,
} from "@mui/material";
import { Box } from "@mui/system";
import { useDispatch, useSelector } from "react-redux";
import { api } from "../models/api";
import { Dispatch, RootState } from "../models/store";
import React, { useEffect } from "react";

export default function ControlPanel() {
  const theme = useTheme<CustomTheme>();
  const hub = useSelector((state: RootState) => state.hub);

  // useEffect(() => {
  //   dispatch.refetch.subscribeHub(5000);
  //   dispatch.refetch.start();
  // }, []);

  const dispatch = useDispatch<Dispatch>();
  let dryThreshold = hub.control.dryThreshold;
  let flowTime = hub.control.flowTime;
  const [_flowTime, setFlowTime] = React.useState(flowTime);
  const [_dryThreshold, setDryThreshold] = React.useState(dryThreshold);

  return (
    <Box sx={{ padding: theme.spacing(3) }}>
      <Grid container spacing={3}>
        <Grid
          item
          container
          direction="column"
          spacing={theme.spacing(3)}
          wrap="nowrap"
          sm={12}
          md={6}
        >
          <Grid item container xs={12} spacing={theme.spacing(3)}>
            <Grid item xs={6}>
              <Card
                onClick={() => dispatch.hub.togglePlanter()}
                sx={{
                  cursor: "pointer",
                  width: "100%",
                  height: 200,
                  display: "flex",
                  justifyContent: "center",
                  alignItems: "center",
                  background: hub.control.planterEnabled
                    ? theme.palette.success.main
                    : theme.palette.error.main,
                  color: hub.control.planterEnabled
                    ? theme.palette.success.contrastText
                    : theme.palette.error.contrastText,
                }}
              >
                <Typography
                  sx={{
                    fontSize: theme.typography.h5.fontSize,
                    textAlign: "center",
                  }}
                >
                  Planter Pumps
                </Typography>
              </Card>
            </Grid>
            <Grid item xs={6}>
              <Card
                onClick={() => dispatch.hub.toggleHydroponic()}
                sx={{
                  cursor: "pointer",
                  width: "100%",
                  height: 200,
                  display: "flex",
                  justifyContent: "center",
                  alignItems: "center",
                  background: hub.control.hydroponicEnabled
                    ? theme.palette.success.main
                    : theme.palette.error.main,
                  color: hub.control.hydroponicEnabled
                    ? theme.palette.success.contrastText
                    : theme.palette.error.contrastText,
                }}
              >
                <Typography
                  sx={{
                    fontSize: theme.typography.h5.fontSize,
                    textAlign: "center",
                  }}
                >
                  Hydroponic Pumps
                </Typography>
              </Card>
            </Grid>
          </Grid>
          <Grid item container xs={12} spacing={theme.spacing(3)}>
            <Grid item xs={12}>
              <Card
                sx={{
                  padding: theme.spacing(3),
                  width: "100%",
                  display: "flex",
                  justifyContent: "center",
                  alignItems: "start",
                }}
              >
                <List
                  sx={{
                    width: "100%",
                  }}
                >
                  <ListItem>
                    <Stack sx={{ width: "100%" }}>
                      <ListItemText primary="Moisture Threshold" />
                      <Slider
                        min={0}
                        max={100}
                        defaultValue={60}
                        value={_dryThreshold}
                        valueLabelDisplay="auto"
                        valueLabelFormat={(value) => `${value}%`}
                        onChangeCommitted={(_, value) => {
                          if (value instanceof Array) {
                            dispatch.hub.setDryThreshold(value[0]);
                          } else {
                            dispatch.hub.setDryThreshold(value);
                          }
                        }}
                        onChange={(_, value) => {
                          if (value instanceof Array) {
                            setDryThreshold(value[0]);
                          } else {
                            setDryThreshold(value);
                          }
                        }}
                      />
                    </Stack>
                  </ListItem>
                  <ListItem>
                    <Stack sx={{ width: "100%" }}>
                      <Typography>Flow Time</Typography>
                      <Slider
                        min={1}
                        max={30}
                        defaultValue={3}
                        value={_flowTime}
                        valueLabelDisplay="auto"
                        valueLabelFormat={(value) => `${value} seconds`}
                        onChange={(_, value) => {
                          if (value instanceof Array) {
                            setFlowTime(value[0]);
                          } else {
                            setFlowTime(value);
                          }
                        }}
                        onChangeCommitted={(_, value) => {
                          if (value instanceof Array) {
                            dispatch.hub.setFlowTime(value[0]);
                          } else {
                            dispatch.hub.setFlowTime(value);
                          }
                        }}
                      />
                    </Stack>
                  </ListItem>
                </List>
              </Card>
            </Grid>
          </Grid>
        </Grid>

        <Grid item sm={12} md={6}>
          <Card sx={{ padding: theme.spacing(3), height: "100%" }}>
            <Stack spacing={theme.spacing(3)}>
              <Typography variant="h5" sx={{ textAlign: "center" }}>
                Calibrate Water Level
              </Typography>
              <Typography variant="body1" sx={{ textAlign: "center" }}>
                Empty the water tank then click the start button to begin
                calibrating. Once the resevoir is full click the stop button to
                finish calibrating.
              </Typography>
              <Grid container>
                <Grid item xs={6}>
                  <Card
                    onClick={() => {
                      dispatch.hub.toggleCalibration(
                        hub.dashboard.waterLevel.distance
                      );
                    }}
                    sx={{
                      cursor: "pointer",
                      width: "100%",
                      height: 200,
                      display: "flex",
                      justifyContent: "center",
                      alignItems: "center",
                      padding: theme.spacing(2),
                      background: hub.control.calibrating
                        ? theme.palette.success.main
                        : theme.palette.info.main,
                      color: hub.control.calibrating
                        ? theme.palette.success.contrastText
                        : theme.palette.info.contrastText,
                    }}
                  >
                    <Typography
                      sx={{
                        fontSize: theme.typography.h5.fontSize,
                        textAlign: "center",
                      }}
                    >
                      {hub.control.calibrating
                        ? "Stop Calibration"
                        : "Calibrate"}
                    </Typography>
                  </Card>
                </Grid>
                <Grid item xs={6}>
                  <Box
                    sx={{
                      cursor: "pointer",
                      width: "100%",
                      height: 200,
                      display: "flex",
                      justifyContent: "center",
                      alignItems: "center",
                    }}
                  >
                    <Box>
                      <Typography>{`Distance: ${hub.dashboard.waterLevel.distance.toFixed(
                        2
                      )} cm`}</Typography>
                      <Typography variant="body1" sx={{ textAlign: "center" }}>
                        {`Height: ${hub.control.resevoirHeight.toFixed(2)} cm`}
                      </Typography>
                    </Box>
                  </Box>
                </Grid>
              </Grid>
            </Stack>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
}
