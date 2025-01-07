import { Box } from "@chakra-ui/react";
import { Header, Uploader, UploaderKey } from "../components";


const Home = () => {
  return (
    <Box>
      <Header />
      <Uploader />
      <UploaderKey />
    </Box>
  )
}

export default Home