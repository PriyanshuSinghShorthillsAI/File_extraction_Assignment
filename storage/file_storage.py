import os
import json
import pandas as pd  # For saving tables as CSV

class FileStorage:
    def __init__(self, output_dir: str):
        self.output_dir = output_dir
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

    def save(self, data, filename: str, data_type: str):
        """Save data based on type: 'text', 'image', 'url', or 'table'."""
        if data_type == 'text':
            self.save_text(data, filename)
        elif data_type == 'image':
            self.save_images(data, filename)
        elif data_type == 'url':
            self.save_urls(data, filename)
        elif data_type == 'table':
            self.save_tables(data, filename)
        else:
            raise ValueError("Unsupported data type. Use 'text', 'image', 'url', or 'table'.")

    def save_text(self, data, filename: str):
        txt_filename = os.path.splitext(filename)[0] + ".txt"
        output_path = os.path.join(self.output_dir, txt_filename)
        with open(output_path, 'w') as f:
            f.write(data)

    def save_images(self, images, filename: str):
        images_dir = os.path.join(self.output_dir, "images")
        if not os.path.exists(images_dir):
            os.makedirs(images_dir)

        metadata = []
        for idx, image_info in enumerate(images):
            image_filename = f"image_{idx + 1}.{image_info['ext']}"
            image_path = os.path.join(images_dir, image_filename)
            with open(image_path, "wb") as img_file:
                img_file.write(image_info["image_data"])

            metadata.append({
                "file_name": image_filename,
                "page_number": image_info["page"],
                "dimensions": image_info["dimensions"]
            })

        metadata_file = os.path.join(images_dir, 'metadata.json')
        with open(metadata_file, 'w') as f:
            json.dump(metadata, f, indent=4)

    def save_urls(self, urls, filename: str):
        urls_dir = os.path.join(self.output_dir, "urls")
        if not os.path.exists(urls_dir):
            os.makedirs(urls_dir)

        url_filename = os.path.join(urls_dir, "urls.txt")
        metadata = []

        with open(url_filename, "w") as url_file:
            for url_info in urls:
                url_file.write(f"{url_info['url']}\n")
                metadata.append({
                    "url": url_info["url"],
                    "page_number": url_info["page"],
                    "position": url_info["position"]
                })

        metadata_file = os.path.join(urls_dir, "metadata.json")
        with open(metadata_file, 'w') as f:
            json.dump(metadata, f, indent=4)

    def save_tables(self, tables, filename: str):
        """Save extracted tables as CSV files."""
        tables_dir = os.path.join(self.output_dir, "tables")
        if not os.path.exists(tables_dir):
            os.makedirs(tables_dir)

        for idx, table_df in enumerate(tables):
            csv_filename = f"table_{idx + 1}.csv"
            csv_path = os.path.join(tables_dir, csv_filename)
            table_df.to_csv(csv_path, index=False)
