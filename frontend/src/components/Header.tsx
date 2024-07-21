import {
  Box,

  Flex,
  Heading,

  Image,
  Text,
} from "@chakra-ui/react";
import { ai } from "../assets";


const Header = () => {
  return (
    <Flex
      direction={{ base: "column", lg: "row" }}
      paddingX="6rem"
      paddingY="2rem"
      marginBottom={10}
    >
      <Box
        marginRight={{ base: "", lg: "5rem" }}
        marginBottom="3rem"
        alignItems="flex-start"
        flex="1"
      >
        <Heading
          as="h1"
          background="gradient"
          backgroundClip="text"
          fontWeight="800"
          fontSize={{ base: "36px", md: "48px", lg: "62px" }}
          lineHeight={{ base: "48px", md: "60px", lg: "75px" }}
          letterSpacing="-0.04em"
          paddingY={{ base: 1, lg: "5rem" }}
        >
          
        </Heading>
        <Text
          fontWeight="400"
          fontSize={{ base: "14px", md: "16px", lg: "20px" }}
          marginTop="-25%"
          lineHeight={{ base: "24px", lg: "28px" }}
          color="text"
        >
          The prototype archive we present here is a glimpse into a future where digital photos are transformed by advanced cryptography and decentralized web protocols.
        </Text>
      
      </Box>
      <Box flex="1">
        <Image  src={ai} alt="ai" width="100%" height="100%" />
      </Box>
    </Flex>
  );
};

export default Header;
