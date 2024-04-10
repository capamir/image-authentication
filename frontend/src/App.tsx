import { Box, ChakraProvider, ColorModeScript } from "@chakra-ui/react";
import { Header } from "./components";
import theme from "./theme";

function App() {
  return (
    <ChakraProvider theme={theme}>
      <ColorModeScript initialColorMode={theme.config.initialColorMode} />
      <Box background="colorBg" fontFamily="var(--font-family)">
        <Header />
      </Box>
    </ChakraProvider>
  );
}

export default App;
