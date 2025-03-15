import axios from "axios";
import {
  Box,
  Button,
  Card,
  CardBody,
  Flex,
  FormControl,
  Heading,
  Image,
  Spinner,
  Text,
  FormLabel,
  Input,
  useToast,
  useColorModeValue,
  useTheme,
} from "@chakra-ui/react";
import { useState } from "react";
import { useDropzone } from "react-dropzone";

const Uploader = () => {
  const theme = useTheme();
  const gradient = useColorModeValue(
    theme.colors.gradient.light, // Light mode gradient
    theme.colors.gradient.dark // Dark mode gradient
  );
  const [file, setFile] = useState<File | undefined>(undefined);
  const [isUploading, setIsUploading] = useState<boolean>(false);
  const [percentage, setPercentage] = useState<string>("");
  const [compressedImageUrl, setCompressedImageUrl] = useState<string>("");
  const [keyFile, setKeyFile] = useState<FileType | null>(null);
  const toast = useToast();

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    accept: "image/*",
    onDrop: (acceptedFiles) => {
      if (acceptedFiles?.length) {
        setFile(
          Object.assign(acceptedFiles[0], {
            preview: URL.createObjectURL(acceptedFiles[0]),
          })
        );
      }
    },
  });

  const handleKeyFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = e.target.files?.[0];
    if (selectedFile) {
      setKeyFile(
        Object.assign(selectedFile, {
          preview: URL.createObjectURL(selectedFile),
        })
      );
    }
  };

  const uploading = async () => {
    if (!file) {
      toast({
        title: "No file selected",
        description: "Please select a file before submitting.",
        status: "warning",
        duration: 5000,
        isClosable: true,
      });
      return;
    }

    if (!keyFile) {
      toast({
        title: "No key file selected",
        description: "Please select a key file before submitting.",
        status: "warning",
        duration: 5000,
        isClosable: true,
      });
      return;
    }

    const formData = new FormData();
    formData.append("image", file as Blob);
    formData.append("percentage", percentage);
    formData.append("file", keyFile); // Use 'file' to match the backend

    setIsUploading(true);
    try {
      const config = {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      };

      const { data } = await axios.post(
        "http://127.0.0.1:8000/api/products/upload/",
        formData,
        config
      );

      if (data) {
        setCompressedImageUrl(`data:image/png;base64,${data.compressed_image}`);
   
        toast({
          title: "Upload successful",
          description: (
            <Box>
              <Text>Percentage: {data.percentage}</Text>
              <Text>Block Index: {data.block_index}</Text>
            </Box>
          ),
          status: "success",
          duration: 5000,
          isClosable: true,
        });
      }
    } catch (error) {
      console.error(
        "Error uploading image:",
        error.response?.data?.error || error.message
      );
      toast({
        title: "Upload failed",
        description:
          error.response?.data?.error ||
          "There was an error uploading your image.",
        status: "error",
        duration: 5000,
        isClosable: true,
      });
    } finally {
      setIsUploading(false);
    }
  };

  const resetFiles = () => {
    setFile(undefined);
    setCompressedImageUrl("");
    setIsUploading(false);
    setKeyFile(null);
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    uploading();
  };

  return (
    <Card
      className="upload__bg"
      width={{ base: "95%", md: "90%", lg: "90%" }}
      marginX="auto"
      padding={{ base: "1.5rem", md: "2rem" }}
      marginY={5}
    >
      <CardBody>
        {/* Heading */}
        <Heading
          background={gradient}
          as="h2"
          backgroundClip="text"
          marginBottom="2rem"
          fontSize={{ base: "24px", md: "28px", lg: "32px" }}
          textAlign="center"
        >
          Image Authentication
        </Heading>

        {/* Form */}
        <form onSubmit={handleSubmit}>
          {/* Drag-and-Drop Box */}
          <FormControl
            marginX="auto"
            p={4}
            border="2px"
            borderColor={isDragActive ? "green.500" : "gray.300"}
            borderStyle="dashed"
            borderRadius="md"
            textAlign="center"
            cursor="pointer"
            height="150px"
            {...getRootProps()}
          >
            <input {...getInputProps()} />
            {isDragActive ? (
              <Text fontSize={{ base: "18px", md: "20px", lg: "22px" }}>
                Drop the image here ...
              </Text>
            ) : (
              <Text fontSize={{ base: "18px", md: "20px", lg: "22px" }}>
                Drag 'n' drop an image here, or click to select from files
              </Text>
            )}
          </FormControl>

          {/* Input for Percentage */}
          <FormControl marginY={5}>
            <FormLabel fontSize={{ base: "14px", md: "16px" }}>
              Adjust the DCT coefficient retention percentage:
            </FormLabel>
            <Input
              type="text"
              value={percentage}
              onChange={(e) => setPercentage(e.target.value)}
            />
          </FormControl>

          {/* Key File Upload */}
          <FormControl marginY={5}>
            <FormLabel fontSize={{ base: "14px", md: "16px" }}>
              Upload your key file:
            </FormLabel>
            <Input type="file" onChange={handleKeyFileChange} padding={2} />
          </FormControl>

          {/* Submit and Reset Buttons */}
          <Flex direction={{ base: "column", sm: "row" }} gap={3} marginTop={2}>
            <Button
              type="submit"
              paddingY="0.5rem"
              paddingX="1rem"
              color="#fff"
              background="#FF4820"
              fontSize="18px"
              lineHeight="25px"
              border="none"
              cursor="pointer"
              borderRadius="md"
              width={{ base: "100%", sm: "auto" }}
            >
              Submit
            </Button>
            <Button
              paddingY="0.5rem"
              paddingX="1rem"
              color="#fff"
              background="#FF4820"
              fontSize="18px"
              lineHeight="25px"
              border="none"
              cursor="pointer"
              borderRadius="md"
              onClick={resetFiles}
              width={{ base: "100%", sm: "auto" }}
            >
              Reset
            </Button>
          </Flex>
        </form>

        {/* Uploaded and Compressed Images Section */}
        <Flex
          direction={{ base: "column", md: "row" }}
          gap={4}
          marginTop="2rem"
          justifyContent="space-between"
        >
          {/* Accepted Files */}
          <Box>
            <Heading
              as="h3"
              fontSize={{ base: "20px", md: "22px" }}
              marginBottom={3}
            >
              Accepted Files
            </Heading>
            {isUploading && <Spinner />}
            {file && (
              <Card width={{ base: "100%", md: "400px" }} marginY={4}>
                <CardBody>
                  <Image
                    src={file.preview}
                    alt="Image"
                        width="100%" // Fill the container
                        height="auto" // Preserve aspect ratio
                        objectFit="contain"
                        borderRadius="md"
                  />
                </CardBody>
              </Card>
            )}
          </Box>

          {/* Compressed Image */}
          <Box>
            <Heading
              as="h3"
              fontSize={{ base: "20px", md: "22px" }}
              marginBottom={3}
            >
              Stored Image
            </Heading>
            {compressedImageUrl && (
              <Card width={{ base: "100%", md: "400px" }} marginY={4} > 
                <CardBody>
                <Image
                        src={compressedImageUrl}
                        alt="compressedImage"
                        width="100%" // Fill the container
                        height="auto" // Preserve aspect ratio
                        objectFit="contain"
                        borderRadius="md"
                    />
             
                </CardBody>
              </Card>
            )}
          </Box>
        </Flex>
      </CardBody>
    </Card>
  );
};

export default Uploader;
