import { Box, Heading, Text, useColorModeValue, useTheme, VStack } from "@chakra-ui/react";

const How = () => {
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
          How It Works
        </Heading>

        <Text fontSize={{ base: "md", lg: "lg" }} lineHeight="1.8">
          In <strong>Image Authentication and Restoration platform</strong>, we ensure the authenticity and integrity of your
          digital images. Here's a step-by-step guide to how our process works:
        </Text>

        <Heading
          as="h2"
          fontSize={{ base: "xl", lg: "2xl" }}
          fontWeight="600"
          color="text"
        >
          Step 1: Encrypt Your Image
        </Heading>

        <Text fontSize={{ base: "md", lg: "lg" }} lineHeight="1.8">
          In the first step, you upload an image to our platform. Using our
          advanced **Discrete Cosine Transform (DCT) algorithm**, we:
        </Text>
        <Box as="ul" paddingLeft="1.5rem">
          <Text as="li" fontSize={{ base: "md", lg: "lg" }} lineHeight="1.8">
            Analyze the image and apply a secure encryption process.
          </Text>
          <Text as="li" fontSize={{ base: "md", lg: "lg" }} lineHeight="1.8">
            Generate a unique encryption key that serves as the key to decrypt
            the image later.
          </Text>
        </Box>
        <Text fontSize={{ base: "md", lg: "lg" }} lineHeight="1.8">
          Once the process is complete, you receive the **encrypted image** and
          its corresponding **decryption key** to ensure the confidentiality of
          your data.
        </Text>

        <Heading
          as="h2"
          fontSize={{ base: "xl", lg: "2xl" }}
          fontWeight="600"
          color="text"
        >
          Step 2: Storing the Image Hash in Blockchain
        </Heading>

        <Text fontSize={{ base: "md", lg: "lg" }} lineHeight="1.8">
          In the second step, the user submits:
        </Text>
        <Box as="ul" paddingLeft="1.5rem">
          <Text as="li" fontSize={{ base: "md", lg: "lg" }} lineHeight="1.8">
            The image whose integrity to be verified.
          </Text>
          <Text as="li" fontSize={{ base: "md", lg: "lg" }} lineHeight="1.8">
            The corresponding **encrypted key**.
          </Text>
        </Box>

        <Text fontSize={{ base: "md", lg: "lg" }} lineHeight="1.8">
          Here's what happens next:
        </Text>
        <Box as="ul" paddingLeft="1.5rem">
          <Text as="li" fontSize={{ base: "md", lg: "lg" }} lineHeight="1.8">
            Our system locates the encrypted image stored in our **blockchain
            backend** using the submitted encryption key.
          </Text>
          <Text as="li" fontSize={{ base: "md", lg: "lg" }} lineHeight="1.8">
            Using the **DCT algorithm**, we compare the submitted image with the
            image whose hash is stored in a block.
          </Text>
          <Text as="li" fontSize={{ base: "md", lg: "lg" }} lineHeight="1.8">
            Any malicious differences between the two images are analyzed and reported to
            verify the authenticity of the original image.
          </Text>
        </Box>

        <Heading
          as="h2"
          fontSize={{ base: "xl", lg: "2xl" }}
          fontWeight="600"
          color="text"
        >
          Why Use Our Service?
        </Heading>

        <Text fontSize={{ base: "md", lg: "lg" }} lineHeight="1.8">
          Our streamlined process leverages blockchain technology for secure
          data storage and retrieval, while our DCT-based analysis ensures
          accurate and reliable results. Whether you want to encrypt your
          images or verify their authenticity, we provide a comprehensive
          solution for all your needs.
        </Text>

        <Text fontSize={{ base: "md", lg: "lg" }} lineHeight="1.8">
          Experience the next level of image security and trust with{" "}
          <strong>Image Authentication Site</strong>.
        </Text>
      </VStack>
    </Box>
  );
};

export default How;
