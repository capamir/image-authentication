import { Box, ChakraProvider, ColorModeScript } from "@chakra-ui/react";
import { Header, Navbar } from "./components";
import theme from "./theme";
import "./App.css";

function App() {
  return (
    <ChakraProvider theme={theme}>
      <ColorModeScript initialColorMode={theme.config.initialColorMode} />
      <Box background="colorBg" fontFamily="var(--font-family)">
        <Box className="gradient__bg">
          <Navbar />
          <Header />
        </Box>
      </Box>
    </ChakraProvider>
  );
}

export default App;
