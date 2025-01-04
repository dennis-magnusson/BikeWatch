import { Listing } from "../types";
import { Card, CardContent, CardHeader, CardTitle } from "./ui/card";

import * as React from "react";

import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { CardFooter } from "@/components/ui/card";
import { ChevronLeft, ChevronRight, ExternalLink } from "lucide-react"; // Import carousel icons

type ListingCardProps = {
    listing: Listing;
};

function ListingCard({ listing }: ListingCardProps) {
    const [selectedImage, setSelectedImage] = React.useState(0);

    const handlePrevImage = () => {
        setSelectedImage((prev) =>
            prev === 0 ? listing.images.length - 1 : prev - 1
        );
    };

    const handleNextImage = () => {
        setSelectedImage((prev) =>
            prev === listing.images.length - 1 ? 0 : prev + 1
        );
    };

    return (
        <Card className="w-[350px]">
            <div className="space-y-2">
                <div className="relative w-full h-48 overflow-hidden">
                    <img
                        src={listing.images[selectedImage]}
                        alt={`Bike image ${selectedImage + 1}`}
                        className="object-cover w-full h-full"
                    />
                    <Badge className="absolute top-2 right-2 text-lg font-bold">
                        {listing.price}€
                    </Badge>
                    <button
                        onClick={handlePrevImage}
                        className="absolute top-1/2 left-2 transform -translate-y-1/2 bg-white p-1 rounded-full"
                    >
                        <ChevronLeft />
                    </button>
                    <button
                        onClick={handleNextImage}
                        className="absolute top-1/2 right-2 transform -translate-y-1/2 bg-white p-1 rounded-full"
                    >
                        <ChevronRight />
                    </button>
                </div>
                <div className="flex justify-center space-x-2 p-2 overflow-x-auto">
                    {listing.images.map((image, index) => (
                        <button
                            key={index}
                            onClick={() => setSelectedImage(index)}
                            className={`w-16 h-12 relative overflow-hidden rounded ${
                                index === selectedImage
                                    ? "ring-2 ring-primary"
                                    : ""
                            }`}
                        >
                            <img
                                src={image}
                                alt={`Thumbnail ${index + 1}`}
                                className="object-cover w-full h-full"
                            />
                        </button>
                    ))}
                </div>
            </div>
            <CardHeader>
                <CardTitle className="text-xl">{listing.title}</CardTitle>
                <p className="text-sm text-muted-foreground">
                    {listing.city}, {listing.region}
                </p>
            </CardHeader>
            <CardContent>
                <p className="text-sm">{listing.size}</p>
            </CardContent>
            <CardFooter>
                <Button
                    variant="outline"
                    className="w-full"
                    as="a"
                    href={listing.url}
                    target="_blank"
                >
                    View on fillaritori.com <ExternalLink />
                </Button>
            </CardFooter>
        </Card>
    );
}

export default ListingCard;
