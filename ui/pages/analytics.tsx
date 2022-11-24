import { Box, useTheme, CustomTheme, Grid } from "@mui/material";
import { SystemPulse, SystemPulseType } from "../components/SystemPulse";
import { WaterConsumption } from "../components/waterConsumption";

export default function AnalyticsPage() {
  const theme = useTheme<CustomTheme>();

  return (
    <Grid container spacing={theme.spacing(3)} direction="column" wrap="nowrap">
      <Grid item>
        <Box
          sx={{
            padding: theme.spacing(3),
          }}
        >
          <Box
            sx={{
              borderRadius: theme.shape.borderRadius,
              background: theme.palette.background.paper,
              padding: theme.spacing(3),
              position: "relative",
            }}
          >
            <WaterConsumption />
          </Box>
        </Box>
      </Grid>
      <Grid item>
        <Box
          sx={{
            padding: theme.spacing(3),
          }}
        >
          <Box
            sx={{
              borderRadius: theme.shape.borderRadius,
              background: theme.palette.background.paper,
              padding: theme.spacing(3),
              position: "relative",
            }}
          >
            <SystemPulse
              types={[
                SystemPulseType.WaterLevel,
                SystemPulseType.AverageMoisture,
              ]}
            />
          </Box>
        </Box>
      </Grid>
      <Grid item>
        <Box
          sx={{
            padding: theme.spacing(3),
          }}
        >
          <Box
            sx={{
              borderRadius: theme.shape.borderRadius,
              background: theme.palette.background.paper,
              padding: theme.spacing(3),
              position: "relative",
            }}
          >
            <SystemPulse
              types={[SystemPulseType.Light, SystemPulseType.Temperature]}
            />
          </Box>
        </Box>
      </Grid>
    </Grid>
  );
}
