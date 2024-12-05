import { Box, Heading, Text, useColorModeValue, useTheme, VStack } from "@chakra-ui/react";

const About = () => {
    const theme = useTheme();
    const gradient = useColorModeValue(
      theme.colors.gradient.light, // Light mode gradient
      theme.colors.gradient.dark   // Dark mode gradient
    );
  return (
    <Box
      paddingX={{ base: "1rem", md: "2rem", lg: "4rem" }}
      paddingY="4rem"
      background="colorBg"
      color="text"
    >
      <VStack spacing={6} align="start" maxWidth="800px" marginX="auto">
        <Heading
          as="h1"
          fontSize={{ base: "2xl", md: "3xl", lg: "4xl" }}
          background={gradient}
          backgroundClip="text"
          fontWeight="800"
          textAlign="left"
        >
          About Us
        </Heading>

        <Text fontSize={{ base: "md", lg: "lg" }} lineHeight="1.8">
          Welcome to <strong>Image Authentication Site</strong>, where
          safeguarding the authenticity of digital images is our mission. In
          today’s digital age, the integrity of visual content has never been
          more critical. We are dedicated to ensuring your images are genuine
          and trustworthy.
        </Text>

        <Heading
          as="h2"
          fontSize={{ base: "xl", lg: "2xl" }}
          fontWeight="600"
          color="text"
          
        >
          Our Expertise
        </Heading>

        <Text fontSize={{ base: "md", lg: "lg" }} lineHeight="1.8">
          With cutting-edge technology and a team of experienced professionals,
          we specialize in:
        </Text>
        <Box as="ul" paddingLeft="1.5rem">
          <Text as="li" fontSize={{ base: "md", lg: "lg" }} lineHeight="1.8">
            <strong>Image Verification:</strong> Advanced tools to detect any
            alterations or tampering.
          </Text>
          <Text as="li" fontSize={{ base: "md", lg: "lg" }} lineHeight="1.8">
            <strong>Authenticity Analysis:</strong> Comprehensive reports that
            validate the originality of your content.
          </Text>
          <Text as="li" fontSize={{ base: "md", lg: "lg" }} lineHeight="1.8">
            <strong>Integrity Protection:</strong> Helping you maintain trust in
            your visual assets.
          </Text>
        </Box>

        <Heading
          as="h2"
          fontSize={{ base: "xl", lg: "2xl" }}
          fontWeight="600"
          color="text"
        >
          Why Choose Us?
        </Heading>
        <Text fontSize={{ base: "md", lg: "lg" }} lineHeight="1.8">
          <strong>Image Authentication Site</strong> is the trusted partner for
          your digital content needs because:
        </Text>
        <Box as="ul" paddingLeft="1.5rem">
          <Text as="li" fontSize={{ base: "md", lg: "lg" }} lineHeight="1.8">
            <strong>Advanced Technology:</strong> Our state-of-the-art
            algorithms provide accurate and reliable results.
          </Text>
          <Text as="li" fontSize={{ base: "md", lg: "lg" }} lineHeight="1.8">
            <strong>Expert Team:</strong> A group of skilled analysts and
            developers ensures every image is thoroughly examined.
          </Text>
          <Text as="li" fontSize={{ base: "md", lg: "lg" }} lineHeight="1.8">
            <strong>Trustworthy Service:</strong> We prioritize transparency and
            deliver results you can count on.
          </Text>
        </Box>

        <Heading
          as="h2"
          fontSize={{ base: "xl", lg: "2xl" }}
          fontWeight="600"
          color="text"
        >
          Our Commitment
        </Heading>
        <Text fontSize={{ base: "md", lg: "lg" }} lineHeight="1.8">
          At <strong>Image Authentication Site</strong>, we understand the value
          of authentic content. Whether you’re a photographer, business owner,
          or digital creator, our services are tailored to protect your images
          from tampering and uphold their credibility.
        </Text>
      </VStack>
    </Box>
  );
};

export default About;
