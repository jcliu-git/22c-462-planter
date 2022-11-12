import dynamic from "next/dynamic";
import React from "react";

export const NonSSRWrapper = (props: React.PropsWithChildren) => (
  <React.Fragment>{props.children}</React.Fragment>
);
export default dynamic(() => Promise.resolve(NonSSRWrapper), {
  ssr: false,
});
