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
          marginTop="-30%"
          lineHeight={{ base: "24px", lg: "28px" }}
          color="white"
        >
        Image Authentication: Secure Your Images with Hash Generation
        Ensure the authenticity and integrity of your images with hash generation. This process creates a unique digital fingerprint for each image, allowing you to detect any unauthorized modifications and protect your digital assets from tampering.        </Text>
      
      </Box>
      
      <Box flex="1" marginLeft='30%'>
        <Image  src={ai} alt="ai" width="400px"  height='300px' margin-left='200px' />
      </Box>
    </Flex>
  );
};

export default Header;
