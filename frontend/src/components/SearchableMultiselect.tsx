import { Check, MapPin, X } from "lucide-react";
import * as React from "react";

import { cn } from ".././lib/utils";
import { Location } from "../types";
import { Badge } from "./ui/badge";
import { Button } from "./ui/button";
import {
    Command,
    CommandEmpty,
    CommandGroup,
    CommandInput,
    CommandItem,
    CommandList,
} from "./ui/command";
import { Popover, PopoverContent, PopoverTrigger } from "./ui/popover";

type SearchableMultiselectProps = {
    locations: Location[];
    locationFilters: Location[];
    setLocationFilters: React.Dispatch<React.SetStateAction<Location[]>>;
};

function SearchableMultiselect({
    locationFilters,
    setLocationFilters,
    locations,
}: SearchableMultiselectProps) {
    const [open, setOpen] = React.useState(false);

    // TODO: Confirm that locations in location array are non-null

    const handleSelect = (currentLocation: Location) => {
        if (currentLocation) {
            setLocationFilters((prev) =>
                prev.includes(currentLocation)
                    ? prev.filter((value) => value !== currentLocation)
                    : [...prev, currentLocation]
            );
        }
    };

    const handleRemove = (locationToRemove: Location) => {
        setLocationFilters((prev) =>
            prev.filter((value) => value !== locationToRemove)
        );
    };

    return (
        <div className="flex flex-col gap-2">
            <Popover open={open} onOpenChange={setOpen}>
                <PopoverTrigger asChild>
                    <Button
                        variant="outline"
                        role="combobox"
                        aria-expanded={open}
                        className="w-full justify-between"
                    >
                        {locationFilters.length > 0
                            ? `${locationFilters.length} selected`
                            : "Filter by location"}
                        <MapPin className="ml-2 h-4 w-4 shrink-0 opacity-50" />
                    </Button>
                </PopoverTrigger>
                <PopoverContent className="w-full p-0">
                    <Command>
                        <CommandInput
                            placeholder="Search cities & regions"
                            className="h-9"
                        />
                        <CommandList>
                            <CommandEmpty>No locations found</CommandEmpty>
                            <CommandGroup>
                                {locations.map((location) => (
                                    <CommandItem
                                        key={location.name}
                                        value={location.name}
                                        onSelect={() => handleSelect(location)}
                                    >
                                        {location.name}
                                        <Check
                                            className={cn(
                                                "ml-auto h-4 w-4",
                                                locationFilters.includes(
                                                    location
                                                )
                                                    ? "opacity-100"
                                                    : "opacity-0"
                                            )}
                                        />
                                    </CommandItem>
                                ))}
                            </CommandGroup>
                        </CommandList>
                    </Command>
                </PopoverContent>
            </Popover>
            <div className="flex flex-wrap gap-2">
                {locationFilters.map((loc) => {
                    const location = locations.find((l) => l === loc);
                    return (
                        <Badge key={loc.name} variant="secondary">
                            {location?.name}
                            <Button
                                variant="ghost"
                                size="sm"
                                className="ml-1 h-auto p-0 text-muted-foreground hover:bg-transparent hover:text-foreground"
                                onClick={() => handleRemove(loc)}
                            >
                                <X className="h-3 w-3" />
                                <span className="sr-only">Remove</span>
                            </Button>
                        </Badge>
                    );
                })}
            </div>
        </div>
    );
}

export default SearchableMultiselect;
