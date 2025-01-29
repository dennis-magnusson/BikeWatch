import { Label } from "@radix-ui/react-label";
import { Copy } from "lucide-react";
import { Button } from "./ui/button";
import {
    Dialog,
    DialogClose,
    DialogContent,
    DialogDescription,
    DialogFooter,
    DialogHeader,
    DialogTitle,
    DialogTrigger,
} from "./ui/dialog";
import { Input } from "./ui/input";

export function SetAlertDialog() {
    const alert_id = "dummy_id";
    const bot_identifier = "dummy_bot";
    const alert_bot_url = `https://t.me/${bot_identifier}?start=${dummy_id}`;

    return (
        <Dialog>
            <DialogTrigger asChild>
                <Button variant="outline">Save search for alerts</Button>
            </DialogTrigger>
            <DialogContent className="sm:max-w-md">
                <DialogHeader>
                    <DialogTitle>Get notifications for this search</DialogTitle>
                    <DialogDescription>
                        Get notifications for new listings that match your
                        search filters via the Telegram bot.
                    </DialogDescription>
                </DialogHeader>
                <div className="flex items-center space-x-2">
                    <div className="grid flex-1 gap-2">
                        <Label htmlFor="link" className="sr-only">
                            Your personal link
                        </Label>
                        <Input
                            id="link"
                            defaultValue={alert_bot_url}
                            readOnly
                        />
                    </div>
                    <Button type="submit" size="sm" className="px-3">
                        <span className="sr-only">Copy</span>
                        <Copy />
                    </Button>
                </div>
                <DialogFooter className="sm:justify-start">
                    <DialogClose asChild>
                        <Button type="button" variant="secondary">
                            Cancel
                        </Button>
                    </DialogClose>
                </DialogFooter>
            </DialogContent>
        </Dialog>
    );
}
