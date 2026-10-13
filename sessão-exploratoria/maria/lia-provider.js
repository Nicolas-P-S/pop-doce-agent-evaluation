class LiaProvider {
  id() { return "lia-api"; }

  async callApi(prompt) {
    const apiUrl = process.env.LIA_API_URL ||
      "https://rm4naioqykxiti2srofnqz6hqa0ctlav.lambda-url.us-east-1.on.aws/";
    const apiKey = process.env.LIA_API_KEY;
    if (!apiKey) return { error: "Configure a variável LIA_API_KEY." };

    const body = { mensagem: String(prompt) };
    if (process.env.LIA_SYSTEM_PROMPT) body.prompt_sistema = process.env.LIA_SYSTEM_PROMPT;

    try {
      const response = await fetch(apiUrl, {
        method: "POST",
        headers: { "Content-Type": "application/json", "x-api-key": apiKey },
        body: JSON.stringify(body)
      });
      const raw = await response.text();
      let data;
      try { data = JSON.parse(raw); }
      catch { return { error: `Resposta não JSON (HTTP ${response.status})`, output: raw }; }
      if (!response.ok) return { error: `Erro HTTP ${response.status}`, output: JSON.stringify(data) };

      return {
        output: JSON.stringify({
          resposta: data.resposta || "",
          sessao: data.sessao || "",
          versao: data.versao || "",
          ferramentas: data.ferramentas || [],
          metricas: data.metricas || []
        }),
        metadata: { versao: data.versao, ferramentas: data.ferramentas, metricas: data.metricas }
      };
    } catch (e) {
      return { error: `Falha na chamada à API: ${e.message}` };
    }
  }
}
module.exports = LiaProvider;
