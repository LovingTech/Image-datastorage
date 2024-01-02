# A Python tool that converts any file into an image

This allows for the representing of data and the layout of data in a file. Allowing the user to see patterns within data structures, or sometimes the lack of. As far as I know it has no real practical purposes other than to look cool and mess around with information in a new way, for example editing files with photo manipulation tools such as GIMP and Photoshop.

## Usage

### Raw Python

I have created some simple examples that demonstrate the the usage of the tool. In `example_encoding.py` users can see how to create a image of their data and in `example_decoding.py` user can see how to convert back their data from an image to the original file (note that the tool only takes the original file name of the file and therefore encoding can be done in folders but the final result will always occur in the directory from which the decoding was run from). I have tested it with a variety of file types, have not yet come across something that doesn't work.

### Docker

By Building from the `dockerfile` or pulling from this github. Running the command

```
docker run -p 8501:8501 -d imagestorage
```

You'll be able to acess the gui for the script. Allowing for easier use.

## Possible applications

These are obscure and mostly likely it will just be used for enjoyment.

- Semi-secure method of transmiting infomation, purely because it is unusual and would impractical to attempt reverse engineering.
- Visual methods for representing compression.
- Serve as tool for students to understand how information is stored in computers.
