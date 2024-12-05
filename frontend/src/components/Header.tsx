import {
  Box,
  Flex,
  Heading,
  Image,
  Text,
  useColorModeValue,
  useTheme,
} from "@chakra-ui/react";
import { ai } from "../assets";

const Header = () => {    
    const theme = useTheme();
    const gradient = useColorModeValue(
      theme.colors.gradient.light, // Light mode gradient
      theme.colors.gradient.dark   // Dark mode gradient
    );
  return (
    <Flex
      direction={{ base: "column", lg: "row" }}
      paddingX={{ base: "2rem", md: "4rem", lg: "6rem" }}
      paddingY={{ base: "2rem", lg: "4rem" }}
      align="center"
      justify="space-between"
      marginBottom="10"
    >
      {/* Left Content */}
      <Box
        flex="1"
        textAlign={{ base: "center", lg: "left" }}
        marginBottom={{ base: "2rem", lg: "0" }}
      >
        <Heading
          as="h1"
          background={gradient}
          backgroundClip="text"
          fontWeight="800"
          fontSize={{ base: "36px", md: "48px", lg: "62px" }}
          lineHeight={{ base: "48px", md: "60px", lg: "75px" }}
          letterSpacing="-0.04em"
          paddingBottom={{ base: "1rem", lg: "2rem" }}
        >
          Image Authentication Made Simple
        </Heading>
        <Text
          fontWeight="400"
          fontSize={{ base: "14px", md: "16px", lg: "20px" }}
          lineHeight={{ base: "24px", lg: "28px" }}
          color="white"
          maxWidth={{ base: "100%", lg: "80%" }}
          marginX={{ base: "auto", lg: "0" }}
        >
          Secure your images with hash generation. This process creates a unique
          digital fingerprint for each image, ensuring the authenticity and
          integrity of your digital assets. Detect unauthorized modifications
          and protect your images from tampering.
        </Text>
      </Box>

      {/* Right Image */}
      <Box
        flex="1"
        display="flex"
        justifyContent={{ base: "center", lg: "flex-end" }}
        alignItems="center"
      >
        <Image
          src={ai}
          alt="AI Illustration"
          width={{ base: "300px", md: "350px", lg: "400px" }}
          height={{ base: "250px", md: "300px", lg: "350px" }}
          objectFit="cover"
        />
      </Box>
    </Flex>
  );
};

export default Header;
