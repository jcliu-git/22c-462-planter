import {
  Box,
  Card,
  CustomTheme,
  Grid,
  Typography,
  useTheme,
} from "@mui/material";
import Image from "next/image";
import { useSelector } from "react-redux";
import { RootState } from "../models/store";

export function TempAndLight() {
  const theme = useTheme<CustomTheme>();
  const temperature = useSelector(
    (state: RootState) => state.hub.dashboard.temperature
  );
  const light = useSelector((state: RootState) => state.hub.dashboard.light);

  let brightness = (light.luminosity / 30000) * 100;
  if (brightness > 100) {
    brightness = 100;
  }
  if (brightness < 0) {
    brightness = 0;
  }

  return (
    <Card
      sx={{
        padding: theme.spacing(3),
        height: "100%",
      }}
    >
      <Grid
        container
        spacing={2}
        alignItems="center"
        justifyContent="space-between"
        height="100%"
      >
        <Grid item xs={6}>
          <Box>
            <Typography
              variant="h3"
              component="span"
              sx={{
                fontSize: {
                  xs: "2rem",
                  sm: "3rem",
                },
              }}
            >
              {temperature.fahrenheit.toFixed(2)}
            </Typography>
            <Typography
              variant="h6"
              component="sup"
              sx={{
                verticalAlign: "top",
                fontSize: {
                  xs: "1rem",
                  sm: "1.5rem",
                },
              }}
            >
              °F
            </Typography>
          </Box>
        </Grid>
        <Grid item xs={6} textAlign="center">
          <Image
            src="/sun.svg"
            alt="sun"
            width={100}
            height={100}
            style={{
              filter: `invert(88%) sepia(100%) saturate(668%) hue-rotate(346deg) brightness(${brightness}%)`,
            }}
          />
        </Grid>
      </Grid>
    </Card>
    // <div>
    //   <h1>Temperature</h1>
    //   <h2>{temperature.fahrenheit.toFixed(2)}°F</h2>
    //   <h1>Luminosity</h1>
    //   <h2>{light.luminosity}</h2>
    // </div>
  );
}
