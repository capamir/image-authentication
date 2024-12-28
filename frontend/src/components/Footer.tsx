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
             
          </Heading>
          <Text fontFamily="fontBody" fontSize="md" color="gray">
          
         </Text>
        </Box>

        <Box>
          <Heading as="h3" fontFamily="fontBold" fontSize="lg" marginBottom={6}>
           
          </Heading>
          <Text fontFamily="fontBody" fontSize="md" color="gray">
           
                 </Text>
                 <Text fontFamily="fontBody" fontSize="md" color="gray">
          
                 </Text>
                 <Text fontFamily="fontBody" fontSize="md" color="gray">
          
                 </Text>

            
           

        
          
        </Box>
      </SimpleGrid>
      <Divider />
      <Flex gap={5} paddingTop={5} direction={{ base: "column", md: "row" }}>
        <Text fontFamily="fontBold" fontSize="md">
          
        </Text>
        <Spacer />
        <Text fontFamily="fontBold" fontSize="md">
          
        </Text>
      </Flex>
    </Box>
  );
};

export default Footer;
