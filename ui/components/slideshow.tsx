import React from "react";
import { Grid, Theme, useTheme } from "@mui/material";
import { Slide } from "react-slideshow-image";
import "react-slideshow-image/dist/styles.css";
import { Subscription } from "rxjs";
import { Dispatch, RootState, store } from "../models/store";
import { NonSSRWrapper } from "../util/next";
import { useDispatch, useSelector } from "react-redux";

let photoDataSubscription: Subscription | null = null;

const Slideshow = () => {
  const theme = useTheme<Theme>();
  const photoData = useSelector(
    (state: RootState) => state.hub.dashboard.photos
  );
  const dispatch = useDispatch<Dispatch>();

  if (!photoData.length) return null;
  return (
    <div
      className="slide-container"
      style={{ width: `${photoData[0].width}px` }}
    >
      <Slide>
        {photoData.map((slideImage, index) => (
          <div className="each-slide" key={index}>
            <div
              style={{
                backgroundImage: `url(${slideImage.filepath})`,
                height: `${slideImage.height}px`,
                backgroundRepeat: "no-repeat",
                backgroundSize: "cover",
              }}
            >
              {/* <span>{slideImage.caption}</span> */}
            </div>
          </div>
        ))}
      </Slide>
    </div>
  );
};
export default Slideshow;
