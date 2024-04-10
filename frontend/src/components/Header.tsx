import { Box, Flex, Heading, Image, Text } from "@chakra-ui/react";
import { ai } from "../assets";

const Header = () => {
  return (
    <Flex
      direction={{ base: "column", lg: "row" }}
      paddingX="6rem"
      paddingY="4rem"
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
          Let&apos;s Build Something amazing with GPT-3 OpenAI
        </Heading>
        <Text
          fontWeight="400"
          fontSize={{ base: "14px", md: "16px", lg: "20px" }}
          lineHeight={{ base: "24px", lg: "28px" }}
          color="text"
        >
          Yet bed any for travelling assistance indulgence unpleasing. Not
          thoughts all exercise blessing. Indulgence way everything joy
          alteration boisterous the attachment. Party we years to order allow
          asked of.
        </Text>
      </Box>
      <Box flex="1">
        <Image src={ai} alt="ai" width="100%" height="100%" />
      </Box>
    </Flex>
  );
};

export default Header;
