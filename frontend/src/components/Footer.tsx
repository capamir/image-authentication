import {
  Box,
  Divider,
  Flex,
  Heading,
  HStack,
  Link,
  SimpleGrid,
  Spacer,
  Text,
} from "@chakra-ui/react";
import { FaTelegram } from "react-icons/fa";

const Footer = () => {
  return (
    <Box paddingX="8%" paddingY={10}>
      <SimpleGrid columns={{ sm: 1, md: 2, lg: 3, xl: 4 }} spacing={8}>
        <Box>
          <Heading as="h3" fontFamily="fontBold" fontSize="lg" marginBottom={6}>
            about us
          </Heading>
          <Text fontFamily="fontBody" fontSize="md" color="gray">
          At Image Authentication Site, we specialize in verifying the authenticity of digital images. Our advanced technology and expert team provide reliable analysis and comprehensive reports to ensure your images are genuine. Trust us to protect the integrity of your visual content.          </Text>
        </Box>

        <Box>
          <Heading as="h3" fontFamily="fontBold" fontSize="lg" marginBottom={6}>
          Our Team
          </Heading>
          <Text fontFamily="fontBody" fontSize="md" color="gray">
          dr.tabatabaie 
                 </Text>
                 <Text fontFamily="fontBody" fontSize="md" color="gray">
          amir
                 </Text>
                 <Text fontFamily="fontBody" fontSize="md" color="gray">
          matin
                 </Text>

            
           

        
          
        </Box>
      </SimpleGrid>
      <Divider />
      <Flex gap={5} paddingTop={5} direction={{ base: "column", md: "row" }}>
        <Text fontFamily="fontBold" fontSize="md">
          our team
        </Text>
        <Spacer />
        <Text fontFamily="fontBold" fontSize="md">
          copyright &copy;
        </Text>
      </Flex>
    </Box>
  );
};

export default Footer;
