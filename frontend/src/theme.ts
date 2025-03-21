import { extendTheme, ThemeConfig } from "@chakra-ui/react";

const config: ThemeConfig = {
  initialColorMode: "dark",
};

const theme = extendTheme({
  config,
  colors: {
    gray: {
      50: "#f9f9f9",
      100: "#ededed",
      200: "#d3d3d3",
      300: "#b3b3b3",
      400: "#a0a0a0",
      500: "#898989",
      600: "#6c6c6c",
      700: "#202020",
      800: "#121212",
      900: "#111",
    },
    text: "#81afdd",
    gradient: {
      light: "linear-gradient(89.97deg, #ae67fa 1.84%, #f49867 102.67%)",
      dark: "linear-gradient(89.97deg, #c084ff 1.84%, #ff6f61 102.67%)",
    },
    colorBg: "#040c18",
    colorFooter: "var(--color-footer)",
  },
  styles: {
    global: {
      body: {
        bg: "colorBg",
        color: "text",
      },
    },
  },
});

export default theme;
