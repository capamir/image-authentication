import { Box, ChakraProvider, ColorModeScript } from "@chakra-ui/react";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import "./App.css";
import { Footer, Navbar } from "./components";
import About from "./pages/About";
import Home from "./pages/Home";
import theme from "./theme";
import How from "./pages/How";
  
function App() {
  return (
    <ChakraProvider theme={theme}>
      <ColorModeScript initialColorMode={theme.config.initialColorMode} />
      <BrowserRouter>
      <Box background="colorBg" fontFamily="var(--font-family)">
          <Navbar />
          <Box className="gradient__bg">
            <Routes>
              {/* Define your routes here */}
              <Route path="/" element={<Home />} />
              <Route path="/about" element={<About />} />
              <Route path="/how" element={<How />} />
            </Routes>
          </Box>
          <Footer />
        </Box>
      </BrowserRouter>
    </ChakraProvider>
  );
}

export default App;
