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
  Spacer,
  Spinner,
  Text,
  FormLabel,
  Input,
  useToast,
} from "@chakra-ui/react";
import { useCallback, useState } from "react";
import { useDropzone } from "react-dropzone";

const Uploader = () => {
  const [file, setFile] = useState<File | undefined>(undefined);
  const [isUploading, setIsUploading] = useState<boolean>(false);
  const [percentage, setPercentage] = useState<string>("");
  const [compressedImageUrl, setCompressedImageUrl] = useState<string>("");
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

    const formData = new FormData();
    formData.append("image", file as Blob);
    formData.append("percentage", percentage);

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
        // Correctly format the Base64 string for the image source
        setCompressedImageUrl(`data:image/png;base64,${data.compressed_image}`);
        toast({
          title: "Upload successful ",
          description: (
            <Box>
              <Text>Percentage: {data.percentage}</Text>
              <Text>Image Key: {data.key}</Text>
              <Text>Block Index: {data.block_index}</Text>
            </Box>
          ),
          status: "success",
          duration: 5000,
          isClosable: true,
        });
      }
    } catch (error) {
      console.error("Error uploading image:", error.response?.data?.error || error.message);
      toast({
        title: "Upload failed",
        description: error.response?.data?.error || "There was an error uploading your image.",
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
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    uploading();
  };

  return (
    <Card
      className="upload__bg"
      width="90%"
      marginX="auto"
      padding="2rem"
      marginY={5}
    >
      <CardBody>
        <Heading
          as="h2"
          background="gradient"
          backgroundClip="text"
          marginBottom="2rem"
        >
          image authentication 
        </Heading>
        <form onSubmit={handleSubmit}>
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
              <Text fontSize="22px">Drop the image here ...</Text>
            ) : (
              <Text fontSize="22px">
                Drag 'n' drop an image here, or click to select from files
              </Text>
            )}
          </FormControl>
          <FormControl marginY={5}>
            <FormLabel>
              Adjust the DCT coefficient retention percentage:{" "}
            </FormLabel>
            <Input
              type="text"
              value={percentage}
              onChange={(e) => setPercentage(e.target.value)}
            />
          </FormControl>

          <Button
            type="submit"
            paddingY="0.5rem"
            paddingX="1rem"
            marginTop={2}
            color="#fff"
            background="#FF4820"
            fontSize="18px"
            lineHeight="25px"
            border="none"
            cursor="pointer"
            borderRadius="md"
          >
            Submit
          </Button>

          <Button
            paddingY="0.5rem"
            paddingX="1rem"
            marginTop={2}
            marginX={3}
            color="#fff"
            background="#FF4820"
            fontSize="18px"
            lineHeight="25px"
            border="none"
            cursor="pointer"
            borderRadius="md"
            onClick={resetFiles}
          >
            Reset
          </Button>
        </form>
        <Flex gap={3} direction={{ base: "column", md: "row" }}>
          <Box>
            <Heading as="h3" fontSize="25px" marginTop={3}>
              Accepted Files
            </Heading>
            {isUploading && <Spinner />}
            {file && (
              <Card width="300px" marginY={4}>
                <CardBody>
                  <Image src={file.preview} alt={file.name} />
                </CardBody>
              </Card>
            )}
          </Box>
          <Spacer />
            <Box>
              <Heading as="h3" fontSize="25px" marginTop={3}>
                 your image
              </Heading>
              {compressedImageUrl && (
                <Card width="300px" marginY={4}>
                  <CardBody>
                    <Image src={compressedImageUrl} alt="compressedImage" />
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