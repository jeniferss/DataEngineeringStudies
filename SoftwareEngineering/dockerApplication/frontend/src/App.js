import React, { useState } from "react";
import { UploadOutlined, RedoOutlined } from "@ant-design/icons";
import { Button, message, Upload, Table } from "antd";

const App = () => {
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);

  const [jsonData, setJsonData] = useState([]);
  const [columns, setColumns] = useState([]);

  const frameStyle = {
    padding: "5% 10%",
  };

  const buttonBlockStyle = {
    display: "flex",
    float: "right",
    margin: "0 0 2% 0",
  };

  const imageStyle = {
    maxWidth: "30%",
    margin: "2%"
  };

  const sendButtonStyle = {
    marginLeft: "5%",
  };

  const refreshButtonStyle = {
    marginLeft: "5%",
    padding: "0 4%",
  };

  const handleUpload = async () => {
    const formData = new FormData();
    formData.append("file", file);

    setUploading(true);

    await fetch("api/fileHandler/", {
      method: "POST",
      body: formData,
    })
      .then(async (res) => {
        if (res.status !== 200) throw new Error();

        const data = await res.json();
        const columnNames = Object.keys(data[0]);

        const columns = columnNames.map((name) => {
          return {
            title: name,
            dataIndex: name,
            key: name,
          };
        });

        setColumns(columns);
        setJsonData(data);
      })
      .then(() => {
        setFile(null);
        message.success("Arquivo enviado com sucesso!");
      })
      .catch(() => {
        message.error("Falha ao enviar arquivo. Tente novamente!");
      })
      .finally(() => {
        setUploading(false);
      });
  };

  const props = {
    onRemove: (file) => {
      setFile(null);
    },
    beforeUpload: (file) => {
      setFile(file);
      return false;
    },
    file,
  };

  return (
    <div style={frameStyle}>
      <h2>Leitor de arquivos JSON</h2>

      <div style={buttonBlockStyle}>
        <Upload {...props} showUploadList={false}>
          <Button size="large" icon={<UploadOutlined />}>
            {file ? file.name : "Arquivo"}
          </Button>
        </Upload>

        <Button
          type="primary"
          size="large"
          onClick={handleUpload}
          disabled={!file}
          loading={uploading}
          style={sendButtonStyle}
        >
          {uploading ? "Processando" : "Enviar"}
        </Button>

        <Button
          size="large"
          icon={<RedoOutlined />}
          disabled={jsonData.length === 0}
          style={refreshButtonStyle}
          onClick={() => setJsonData([])}
        ></Button>
      </div>

      <div>
        {jsonData.length > 0 ? (
          <Table columns={columns} dataSource={jsonData} />
        ) : (
          <div>
            <h5>Sem dados para mostar.</h5>
            <img alt="no data" style={imageStyle} src="/undraw_taken_re_yn20.svg"></img>
          </div>
        )}
      </div>
    </div>
  );
};

export default App;
